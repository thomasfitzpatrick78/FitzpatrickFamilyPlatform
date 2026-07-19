# Platform Engineering Automation

This directory contains the independent Platform Engineering Automation foundation.

It provides deterministic repository validation, governance validation, release readiness, milestone closeout, engineering metrics, AI Session Readiness validation, governed execution-data validation, and reports for the Fitzpatrick Family Platform repository.

`./platform-eap engineering metrics` reads the latest governed AI Session Readiness JSON report. It does not silently run the readiness validator. Missing or malformed evidence is reported as `UNKNOWN` with guidance to run `./platform-eap ai-session readiness`.

The EO-14.1A Execution Capability adds only data validation and rendering:

```text
./platform-eap execution assignment validate <repository-json-path>
./platform-eap execution completion validate <repository-json-path>
./platform-eap execution completion render <repository-json-path>
```

These commands accept repository-local JSON, reject unknown or executable directive fields, and never execute assignment content, select work, write output files, commit, push, activate services, or alter infrastructure. See [Execution Capability Usage](../docs/engineering-organization/Execution_Capability_Usage.md).
