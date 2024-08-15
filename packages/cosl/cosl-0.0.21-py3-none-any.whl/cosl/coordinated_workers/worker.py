#!/usr/bin/env python3
# Copyright 2024 Canonical Ltd.
# See LICENSE file for licensing details.
"""Generic worker for a distributed charm deployment."""

import logging
import re
import socket
from functools import partial
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple, TypedDict

import ops
import yaml
from ops.model import ActiveStatus, BlockedStatus, WaitingStatus
from ops.pebble import Layer, PathError, ProtocolError

from cosl import JujuTopology
from cosl.coordinated_workers.interface import ClusterRequirer
from cosl.helpers import check_libs_installed

check_libs_installed(
    "charms.loki_k8s.v1.loki_push_api",
)

from charms.loki_k8s.v1.loki_push_api import _PebbleLogClient  # type: ignore

BASE_DIR = "/worker"
CONFIG_FILE = "/etc/worker/config.yaml"
CERT_FILE = "/etc/worker/server.cert"
KEY_FILE = "/etc/worker/private.key"
CLIENT_CA_FILE = "/etc/worker/ca.cert"

logger = logging.getLogger(__name__)

_EndpointMapping = TypedDict("_EndpointMapping", {"cluster": str}, total=True)
"""Mapping of the relation endpoint names that the charms uses, as defined in metadata.yaml."""

ROOT_CA_CERT = Path("/usr/local/share/ca-certificates/ca.crt")


class WorkerError(Exception):
    """Base class for exceptions raised by this module."""


class Worker(ops.Object):
    """Charming worker."""

    _endpoints: _EndpointMapping = {
        "cluster": "cluster",
    }

    def __init__(
        self,
        charm: ops.CharmBase,
        name: str,
        pebble_layer: Callable[["Worker"], Layer],
        endpoints: _EndpointMapping,
    ):
        """Constructor for a Worker object.

        Args:
            charm: The worker charm object.
            name: The name of the workload container and service.
            pebble_layer: The pebble layer of the workload.
            endpoints: Endpoint names for coordinator relations, as defined in metadata.yaml.
        """
        super().__init__(charm, key="worker")
        self._charm = charm
        self._name = name
        self._pebble_layer = partial(pebble_layer, self)
        self.topology = JujuTopology.from_charm(self._charm)
        self._container = self._charm.unit.get_container(name)

        self._endpoints = endpoints

        self.cluster = ClusterRequirer(
            charm=self._charm,
            endpoint=self._endpoints["cluster"],
        )

        self._log_forwarder = ManualLogForwarder(
            charm=self._charm,
            loki_endpoints=self.cluster.get_loki_endpoints(),
            refresh_events=[
                self.cluster.on.config_received,
                self.cluster.on.created,
                self.cluster.on.removed,
            ],
        )

        # Event listeners
        self.framework.observe(self._charm.on.config_changed, self._on_config_changed)
        self.framework.observe(self._charm.on.upgrade_charm, self._on_upgrade_charm)
        self.framework.observe(self._charm.on.collect_unit_status, self._on_collect_status)

        self.framework.observe(self.cluster.on.config_received, self._on_worker_config_received)
        self.framework.observe(self.cluster.on.created, self._on_cluster_created)
        self.framework.observe(self.cluster.on.removed, self._log_forwarder.disable_logging)

        self.framework.observe(self._charm.on[self._name].pebble_ready, self._on_pebble_ready)

    # Event handlers

    def _on_pebble_ready(self, _: ops.PebbleReadyEvent):
        self._charm.unit.set_workload_version(self.running_version() or "")
        self._update_config()

    def _on_worker_config_received(self, _: ops.EventBase):
        self._update_config()

    def _on_upgrade_charm(self, _: ops.UpgradeCharmEvent):
        self._update_cluster_relation()

    def _on_cluster_created(self, _: ops.EventBase):
        self._update_cluster_relation()
        self._update_config()

    def _on_cluster_changed(self, _: ops.EventBase):
        self._update_config()

    def _on_config_changed(self, _: ops.ConfigChangedEvent):
        # If the user has changed roles, publish them to relation data
        self._update_cluster_relation()
        # If there is a config, start the worker
        if self.cluster.get_worker_config():
            self._update_worker_config()

    def _on_collect_status(self, e: ops.CollectStatusEvent):
        if not self._container.can_connect():
            e.add_status(WaitingStatus(f"Waiting for `{self._name}` container"))
        if not self.model.get_relation(self._endpoints["cluster"]):
            e.add_status(BlockedStatus("Missing relation to a coordinator charm"))
        elif not self.cluster.relation:
            e.add_status(WaitingStatus("Cluster relation not ready"))
        if not self.cluster.get_worker_config():
            e.add_status(WaitingStatus("Waiting for coordinator to publish a config"))
        if not self.roles:
            e.add_status(
                BlockedStatus("Invalid or no roles assigned: please configure some valid roles")
            )
        e.add_status(
            ActiveStatus(
                "(all roles) ready."
                if ",".join(self.roles) == "all"
                else f"{','.join(self.roles)} ready."
            )
        )

    # Utility functions
    @property
    def roles(self) -> List[str]:
        """Return a list of the roles this worker should take on.

        Expects that the charm defines a set of roles by config like:
            "role-a": bool
            "role-b": bool
            "role-b": bool
        If this is not the case, it will raise an error.
        """
        config = self._charm.config

        role_config_options = [option for option in config.keys() if option.startswith("role-")]
        if not role_config_options:
            raise WorkerError(
                "The charm should define a set of `role-X` config "
                "options for it to use the Worker."
            )

        active_roles: List[str] = [
            role[5:] for role in role_config_options if config[role] is True
        ]
        return active_roles

    def _update_config(self) -> None:
        """Update the worker config and restart the workload if necessary."""
        restart = any(
            [
                self._update_tls_certificates(),
                self._update_worker_config(),
                self._set_pebble_layer(),
            ]
        )

        if restart:
            self.restart()

    def _set_pebble_layer(self) -> bool:
        """Set Pebble layer.

        Returns: True if Pebble layer was added, otherwise False.
        """
        if not self._container.can_connect():
            return False
        if not self.roles:
            return False

        current_layer = self._container.get_plan()
        new_layer = self._pebble_layer()

        if (
            "services" not in current_layer.to_dict()
            or current_layer.services != new_layer.services
        ):
            self._container.add_layer(self._name, new_layer, combine=True)
            return True

        return False

    def _update_cluster_relation(self) -> None:
        """Publish all the worker information to relation data."""
        self.cluster.publish_unit_address(socket.getfqdn())
        if self._charm.unit.is_leader() and self.roles:
            logger.info(f"publishing roles: {self.roles}")
            self.cluster.publish_app_roles(self.roles)

        if self.cluster.get_worker_config():
            self._update_config()

    def _running_worker_config(self) -> Optional[Dict[str, Any]]:
        """Return the worker config as dict, or None if retrieval failed."""
        if not self._container.can_connect():
            logger.debug("Could not connect to the workload container")
            return None

        try:
            raw_current = self._container.pull(CONFIG_FILE).read()
            return yaml.safe_load(raw_current)
        except (ProtocolError, PathError) as e:
            logger.warning(
                "Could not check the current worker configuration due to "
                "a failure in retrieving the file: %s",
                e,
            )
            return None

    def _update_worker_config(self) -> bool:
        """Set worker config for the workload.

        Returns: True if config has changed, otherwise False.
        Raises: BlockedStatusError exception if PebbleError, ProtocolError, PathError exceptions
            are raised by container.remove_path
        """
        if not self._container.can_connect():
            logger.warning("cannot update worker config: container cannot connect.")
            return False

        if len(self.roles) == 0:
            logger.warning("cannot update worker config: role missing or misconfigured.")
            return False

        worker_config = self.cluster.get_worker_config()
        if not worker_config:
            logger.warning("cannot update worker config: coordinator hasn't published one yet.")
            return False

        if self._running_worker_config() != worker_config:
            config_as_yaml = yaml.safe_dump(worker_config)
            self._container.push(CONFIG_FILE, config_as_yaml, make_dirs=True)
            logger.info("Pushed new worker configuration")
            return True

        return False

    def _update_tls_certificates(self) -> bool:
        """Update the TLS certificates on disk according to their availability."""
        if not self._container.can_connect():
            return False

        if tls_data := self.cluster.get_tls_data():
            private_key_secret = self.model.get_secret(id=tls_data["privkey_secret_id"])
            private_key = private_key_secret.get_content().get("private-key")

            ca_cert = tls_data["ca_cert"]
            server_cert = tls_data["server_cert"]

            # Save the workload certificates
            self._container.push(CERT_FILE, server_cert or "", make_dirs=True)
            self._container.push(KEY_FILE, private_key or "", make_dirs=True)
            self._container.push(CLIENT_CA_FILE, ca_cert or "", make_dirs=True)
            self._container.push(ROOT_CA_CERT, ca_cert or "", make_dirs=True)

            # Save the cacert in the charm container for charm traces
            ROOT_CA_CERT.write_text(ca_cert)
        else:
            self._container.remove_path(CERT_FILE, recursive=True)
            self._container.remove_path(KEY_FILE, recursive=True)
            self._container.remove_path(CLIENT_CA_FILE, recursive=True)
            self._container.remove_path(ROOT_CA_CERT, recursive=True)

            # Remove from charm container
            ROOT_CA_CERT.unlink(missing_ok=True)

        # FIXME: uncomment as soon as the nginx image contains the ca-certificates package
        # self._container.exec(["update-ca-certificates", "--fresh"]).wait()
        # subprocess.run(["update-ca-certificates", "--fresh"])

        return True

    def restart(self):
        """Restart the pebble service or start if not already running."""
        if not self._container.exists(CONFIG_FILE):
            logger.error("cannot restart worker: config file doesn't exist (yet).")
            return

        if not self.roles:
            logger.debug("cannot restart worker: no roles have been configured.")
            return

        try:
            self._container.restart(self._name)
        except ops.pebble.ChangeError as e:
            logger.error(f"failed to (re)start worker job: {e}", exc_info=True)
            return

    def running_version(self) -> Optional[str]:
        """Get the running version from the worker process."""
        if not self._container.can_connect():
            return None

        version_output, _ = self._container.exec([f"/bin/{self._name}", "-version"]).wait_output()
        # Output looks like this:
        # <WORKLOAD_NAME>, version 2.4.0 (branch: HEAD, revision 32137ee...)
        if result := re.search(r"[Vv]ersion:?\s*(\S+)", version_output):
            return result.group(1)
        return None

    def charm_tracing_config(self) -> Tuple[Optional[str], Optional[str]]:
        """Get the charm tracing configuration from the coordinator.

        Usage:
          assuming you are using charm_tracing >= v1.9:
        >>> from ops import CharmBase
        >>> from lib.charms.tempo_k8s.v1.charm_tracing import trace_charm
        >>> from lib.charms.tempo_k8s.v2.tracing import charm_tracing_config
        >>> @trace_charm(tracing_endpoint="my_endpoint", cert_path="cert_path")
        >>> class MyCharm(CharmBase):
        >>>     def __init__(self, ...):
        >>>         self.worker = Worker(...)
        >>>         self.my_endpoint, self.cert_path = self.worker.charm_tracing_config()
        """
        receivers = self.cluster.get_tracing_receivers()

        if not receivers:
            return None, None

        endpoint = receivers.get("otlp_http")
        if not endpoint:
            return None, None

        is_https = endpoint.startswith("https://")

        tls_data = self.cluster.get_tls_data()
        server_ca_cert = tls_data.get("server_cert") if tls_data else None

        if is_https:
            if server_ca_cert is None:
                raise RuntimeError(
                    "Cannot send traces to an https endpoint without a certificate."
                )
            elif not ROOT_CA_CERT.exists():
                # if endpoint is https and we have a tls integration BUT we don't have the
                # server_cert on disk yet (this could race with _update_tls_certificates):
                # put it there and proceed
                ROOT_CA_CERT.parent.mkdir(parents=True, exist_ok=True)
                ROOT_CA_CERT.write_text(server_ca_cert)

            return endpoint, str(ROOT_CA_CERT)
        else:
            return endpoint, None


class ManualLogForwarder(ops.Object):
    """Forward the standard outputs of all workloads to explictly-provided Loki endpoints."""

    def __init__(
        self,
        charm: ops.CharmBase,
        *,
        loki_endpoints: Optional[Dict[str, str]],
        refresh_events: Optional[List[ops.BoundEvent]] = None,
    ):
        _PebbleLogClient.check_juju_version()
        super().__init__(charm, "worker-log-forwarder")
        self._charm = charm
        self._loki_endpoints = loki_endpoints
        self._topology: JujuTopology = JujuTopology.from_charm(charm)

        if not refresh_events:
            return

        for event in refresh_events:
            self.framework.observe(event, self.update_logging)

    def update_logging(self, _: Optional[ops.EventBase] = None):
        """Update the log forwarding to match the active Loki endpoints."""
        loki_endpoints = self._loki_endpoints

        if not loki_endpoints:
            logger.warning("No Loki endpoints available")
            loki_endpoints = {}

        for container in self._charm.unit.containers.values():
            if container.can_connect():
                _PebbleLogClient.disable_inactive_endpoints(  # type:ignore
                    container=container,
                    active_endpoints=loki_endpoints,
                    topology=self._topology,
                )
                _PebbleLogClient.enable_endpoints(  # type:ignore
                    container=container, active_endpoints=loki_endpoints, topology=self._topology
                )

    def disable_logging(self, _: Optional[ops.EventBase] = None):
        """Disable all log forwarding."""
        # This is currently necessary because, after a relation broken, the charm can still see
        # the Loki endpoints in the relation data.
        for container in self._charm.unit.containers.values():
            if container.can_connect():
                _PebbleLogClient.disable_inactive_endpoints(  # type:ignore
                    container=container, active_endpoints={}, topology=self._topology
                )
