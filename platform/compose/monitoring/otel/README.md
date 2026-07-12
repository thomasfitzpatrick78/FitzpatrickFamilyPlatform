# OpenTelemetry Docker Stats Collector

**Lifecycle state:** implementation-ready; not deployed; live metric inventory required.

This package prepares `otel/opentelemetry-collector-contrib:0.156.0` to collect Docker Stats receiver metrics through the internal `docker-api-proxy` service. The Collector does not mount the Docker socket and does not publish a host port. Prometheus scrapes the Collector's internal Prometheus-format endpoint at `otel-docker-stats:9464`.

The Docker Stats receiver is configured with automatic Docker API version negotiation, a 15-second collection interval, and an explicit Docker label allowlist:

- `com.docker.compose.project` -> `docker_compose_project`
- `com.docker.compose.service` -> `docker_compose_service`
- `com.docker.compose.container-number` -> `docker_compose_container_number`

No environment variables, command arguments, raw metadata, host paths, logs, traces, or external telemetry exports are configured. Exact Prometheus metric names and final dashboard PromQL remain provisional until live inventory proves the emitted names and labels on the Beelink Docker 29.6.1 baseline.
