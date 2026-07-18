# Platform Engineering Automation

This directory contains the independent Platform Engineering Automation foundation.

It provides deterministic repository validation, governance validation, release readiness, milestone closeout, engineering metrics, AI Session Readiness validation, and reports for the Fitzpatrick Family Platform repository.

`./platform-eap engineering metrics` reads the latest governed AI Session Readiness JSON report. It does not silently run the readiness validator. Missing or malformed evidence is reported as `UNKNOWN` with guidance to run `./platform-eap ai-session readiness`.
