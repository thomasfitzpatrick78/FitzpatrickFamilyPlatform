# Platform Authentication Boundary Specification

**Document Version:** 1.1

**Status:** Draft for Architecture Gatekeeper Review

**Milestone:** PLAT-14.4

---

## Purpose

Define the Platform-owned authentication boundary required by FFFA-14.2B before the responsive web summary can handle real household financial data.

This specification does not select an identity product, deploy a reverse proxy, create credentials, issue certificates, or authorize live infrastructure changes.

---

## Architecture Boundary

```text
Household Browser
        |
        v
Platform Reverse Proxy / Authentication Boundary
        |
        | verified identity
        v
FFFA Responsive Web Application
        |
        | FFFA-owned permission enforcement
        v
Governed Reporting Services
```

---

## Platform Ownership

The Platform owns:

- Local reverse proxy authentication boundary.
- Identity-header trust boundary.
- HTTPS certificate lifecycle.
- Network access restrictions.
- Future shared identity-service evolution.
- Authentication service monitoring.
- Authentication backup and recovery.
- Platform-owned identity creation, identity removal, authentication credential, authentication recovery, reverse proxy, identity provider, certificate, authentication monitoring, and authentication incident-response operations.
- Security incident and access-revocation procedures.

The Platform does not own FFFA financial roles, permission definitions, role-to-permission mappings, authenticated-identity-to-role mappings, report authorization, financial-data access rules, workbook-download authorization, FFFA access revocation, or customer-facing access behavior.

---

## Authentication Requirements

- Tom and Chris receive individual identities.
- No shared household account.
- FFFA does not directly own long-term password management.
- Architecture should support future migration to a centralized OpenID Connect-compatible identity service.
- No specific identity product is selected by this specification.
- No credentials are created by this specification.

---

## Direct-Access Prevention

- Browser traffic enters through the approved reverse proxy.
- The FFFA service is not directly reachable by household clients.
- Trusted identity headers cannot be supplied by arbitrary clients.
- FFFA accepts identity information only from the trusted proxy boundary.
- Network policy, binding configuration, firewall rules, or equivalent controls prevent bypass.
- Header trust and proxy configuration are explicitly tested.

---

## Network Exposure

Initial release requirements:

- Household-LAN access only.
- No public internet exposure.
- No public DNS requirement.
- No router port forwarding.
- No direct WAN ingress.
- No public reverse proxy.
- Remote access deferred.
- Future remote access requires separate architecture and security approval.

---

## HTTPS and Certificates

HTTPS is required for real household financial data.

A locally trusted certificate model is required. Permanent browser certificate warnings are not acceptable.

The implementation package must address certificate issuance, trust, rotation, backup, recovery, and rollback. Certificates are not deployed by this specification.

---

## Session and Authentication Controls

Platform-owned authentication components must support:

- Inactivity timeout of 30 minutes.
- Absolute session lifetime of 8 hours.
- Explicit logout.
- Secure cookies.
- HTTP-only cookies.
- Appropriate SameSite setting.
- Session identifier rotation after authentication.
- No authentication token storage in browser local storage.
- Session invalidation after access revocation.
- CSRF protections where state-changing authentication operations exist.
- Rate limiting or equivalent protection for authentication attempts.

If browser-close invalidation cannot be guaranteed reliably, implementation evidence must document practical behavior rather than claim it as guaranteed.

---

## Authentication Secrets

The eventual authentication component must:

- Use modern adaptive password hashing if it manages local passwords.
- Never store plaintext or reversibly encrypted passwords.
- Never commit passwords, password hashes, tokens, private keys, or recovery codes to a repository.
- Support Platform identity access revocation.
- Avoid password hints and security questions.
- Support a governed administrator-mediated recovery process for the initial local deployment.

---

## Audit Events

The authentication boundary should record useful security-relevant events:

- Successful login.
- Failed login.
- Logout.
- Session expiration.
- Access revocation.
- User-administration changes.
- Authorization denial if surfaced at the boundary.

Audit data may include user identity, event type, timestamp, outcome, application version, and source address where justified.

Audit data must not include account numbers, transaction amounts, balances, merchant names, report content, workbook contents, passwords, tokens, or session secrets.

---

## Operations and Failure Behavior

Default to deny access when authentication or trusted identity validation fails.

The implementation package must define behavior when:

- Authentication component is unavailable.
- Reverse proxy cannot validate identity.
- FFFA receives no trusted identity.
- FFFA receives an unknown user.
- Platform identity access is revoked.
- FFFA revokes a role mapping for an authenticated identity.
- Certificate is expired or untrusted.
- Authentication backup or restore is required.

---

## Acceptance Criteria

PLAT-14.4 is ready for implementation planning when:

- Reverse proxy architecture and identity-header controls are approved.
- Network controls prevent direct FFFA access.
- LAN-only HTTPS certificate lifecycle is specified.
- Monitoring, backup, recovery, rollback, authentication incident, Platform identity revocation, and FFFA role-mapping revocation handoff procedures are specified.
- FFFA authorization remains owned by FFFA.
- No credentials, certificates, live services, or production changes are created.

---

## Related Documents

- [Milestone 14 Portfolio Plan](../milestones/Milestone_14/Milestone_14_Portfolio_Plan.md)
- [Platform Authentication Boundary Implementation Package](../milestones/Milestone_14/Platform_Authentication_Boundary_Implementation_Package.md)

---

## Revision History

| Version | Description |
|---------|-------------|
| 1.1 | Clarified Platform identity ownership versus FFFA authorization ownership. |
| 1.0 | Initial Platform authentication boundary specification for FFFA-14.2B. |
