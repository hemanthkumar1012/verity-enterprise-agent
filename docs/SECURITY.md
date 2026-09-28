# Security Model

Security is a first-class design constraint for Verity.

## Initial rules

- Secrets are supplied through environment variables and are never committed.
- Tool access will be allowlisted.
- SQL access will use parameterized queries and read-only defaults.
- Human approval will be required before high-impact actions.
- Retrieval will carry source and access metadata.
- Agent actions will be auditable.
- External content will be treated as untrusted input.
- Prompt-injection defenses will be applied at trust boundaries.

Future milestones will add authentication, authorization, tenant isolation, rate limits, audit storage, secret management, and adversarial evaluation.
