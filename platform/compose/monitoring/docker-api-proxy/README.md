# Docker API Proxy

**Lifecycle state:** implementation-ready; not deployed; Architecture Gatekeeper review required before live use.

This package prepares `tecnativa/docker-socket-proxy:0.4.2` as the only service with Docker socket access. The socket is mounted read-only into the proxy. The proxy has no host-published port and is reachable only on the `platform-monitoring` Docker network.

Allowed API capability groups:

- `PING=1`: Docker API liveness and negotiation preflight.
- `VERSION=1`: Docker API version discovery.
- `INFO=1`: daemon metadata needed for compatibility verification.
- `CONTAINERS=1`: container list, inspect, and stats read surfaces needed by the Docker Stats receiver.

Denied API capability groups include `AUTH`, `BUILD`, `COMMIT`, `CONFIGS`, `DISTRIBUTION`, `EVENTS`, `EXEC`, `GRPC`, `IMAGES`, `NETWORKS`, `NODES`, `PLUGINS`, `POST`, `SECRETS`, `SERVICES`, `SESSION`, `SWARM`, `SYSTEM`, `TASKS`, `VOLUMES`, and container mutation helpers such as start, stop, restart, pause, and unpause.

A proxy reduces Docker API exposure but does not make Docker socket access risk-free. Live proof must verify both allowed read behavior and denied mutation or management behavior before the service can advance beyond implementation-ready.
