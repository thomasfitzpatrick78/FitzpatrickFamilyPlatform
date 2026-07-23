# Deployment Configuration Repository Usage

**Document Version:** 1.0

**Status:** Active Repository-Only Usage Guide

## Purpose

This guide describes how to inspect and validate governed deployment-configuration fixtures. Every command is deterministic and repository-only. None contacts Docker, opens a socket, creates a listener, uses networking, loads credentials or certificates, selects a Registry target, deploys software, or changes infrastructure.

## Commands

Run commands from the repository root:

```text
./platform-eap deployment contract
./platform-eap deployment validate
./platform-eap deployment validate valid_repository
./platform-eap deployment digest RepositoryOnly
./platform-eap deployment profile FutureProduction
./platform-eap deployment compatibility RepositoryOnly
./platform-eap deployment fixtures
./platform-eap deployment identity RepositoryOnly
./platform-eap deployment runtime RepositoryOnly
./platform-eap deployment security RepositoryOnly
./platform-eap deployment bundle RepositoryOnly
```

Supported profile names are `RepositoryOnly`, `FutureDevelopment`, `FutureValidation`, and `FutureProduction`. They are descriptive only and always report deployment and execution as disabled.

`deployment validate` evaluates the governed repository bundle. Supplying a fixture scenario evaluates that deterministic positive or negative case. A nonzero result represents strict validation failure; it never attempts remediation or deployment.

`deployment digest` renders the canonical SHA-256 content digest. The digest binds configuration content but is not approval, authentication, authorization, or a cryptographic signature.

`deployment compatibility` reports exact contract-version compatibility. It does not probe an installed provider or runtime.

## Fixture Rules

The fixture library is fixed at `engineering/tests/fixtures/deployment_configuration`. It rejects traversal, symlinks, and oversized input. Repository fixtures use synthetic service identities, approvals, validity windows, and targets only. They contain no authoritative Registry record or captured live-provider response.

Positive fixtures cover repository, future development, future validation, and future production profiles. Negative fixtures cover incompatible or unsupported versions, invalid or wildcard identity, missing policy/audit/limits, excessive or invalid resources, digest mismatch, prohibited enablement, malformed JSON, duplicate fields, and unknown fields.

## Validation Boundary

The commands prove configuration contract integrity, policy alignment, version compatibility, and deterministic rendering. They do not prove runtime enforcement, deployment safety, current Docker compatibility, credential handling, mTLS, target eligibility, live reachability, observation correctness, or activation readiness.

## Change History

| Version | Change |
|---------|--------|
| 1.0 | Added repository-only commands and fixture usage for deployment configuration validation. |
