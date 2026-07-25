# Platform Engineering Automation

This directory contains the independent Platform Engineering Automation foundation.

It provides deterministic repository validation, governance validation, release readiness, milestone closeout, engineering metrics, AI Session Readiness validation, governed execution-data validation, and reports for the Fitzpatrick Family Platform repository.

EO-15.1 adds two read-only repository-governed commands:

```text
./platform-eap ai-session baseline --work-package docs/milestones/Milestone_15/EO_15_1_Engineering_Lifecycle_Transition_Review_Operationalization_Work_Package.md
./platform-eap ai-session baseline --work-package docs/milestones/Milestone_15/EO_15_1_Engineering_Lifecycle_Transition_Review_Operationalization_Work_Package.md --json
./platform-eap milestone transition-review docs/milestones/Milestone_14/Milestone_14_Transition_Review.md
```

The baseline classifier returns `Clean`, `Expected Generated Evidence`, or `Dirty`. Expected generated evidence is limited to the two unstaged readiness outputs and requires current-HEAD attribution, zero readiness errors, current authority, byte-for-byte reproduction from the governed producer, and exactly one permission declaration with the exact value `Permitted` in the canonical tracked work package passed to `--work-package`. Missing context, missing, invalid, duplicate, or conflicting metadata, and `Prohibited` fail closed to `Dirty`. The Transition Review command validates the six approved sections, their order, and substantive content; it does not approve architecture, product, milestone closeout, release, or live work.

`./platform-eap engineering metrics` reads the latest governed AI Session Readiness JSON report. It does not silently run the readiness validator. Missing or malformed evidence is reported as `UNKNOWN` with guidance to run `./platform-eap ai-session readiness`.

The EO-14.1A Execution Capability adds only data validation and rendering:

```text
./platform-eap execution assignment validate <repository-json-path>
./platform-eap execution completion validate <repository-json-path>
./platform-eap execution completion render <repository-json-path>
```

These commands accept repository-local JSON, reject unknown or executable directive fields, and never execute assignment content, select work, write output files, commit, push, activate services, or alter infrastructure. See [Execution Capability Usage](../docs/engineering-organization/Execution_Capability_Usage.md).

The repository-only Production Provider Adapter Foundation adds strict contract inspection, fixture validation, normalization, and deterministic mock commands:

```text
./platform-eap provider contract
./platform-eap provider capabilities
./platform-eap provider fixtures
./platform-eap provider validate request engineering/tests/fixtures/provider_adapter/provider-request.json
./platform-eap provider normalize engineering/tests/fixtures/provider_adapter/provider-request.json healthy_lifecycle
./platform-eap provider mock provider_unavailable engineering/tests/fixtures/provider_adapter/provider-request.json
```

These commands are restricted to governed synthetic fixtures. They do not connect to providers, Docker, sockets, HTTP, hosts, or infrastructure and do not calculate health or activate any capability. See [Production Provider Adapter Repository Usage](../docs/architecture/Production_Provider_Adapter_Repository_Usage.md).
