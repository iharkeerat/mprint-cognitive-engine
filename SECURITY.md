# Security and data-handling notes

**Development prototype — not production-ready.** The application includes user accounts, session persistence, graph access and optional external AI calls. These features have not undergone an independent security review.

- Use environment variables for all real API keys, Neo4j passwords and JWT secrets. Never commit `.env`, credentials, exported student records or production logs.
- The current code includes a development JWT secret fallback and permissive CORS configuration. **Do not deploy publicly** without removing insecure defaults, reviewing authentication/authorization, restricting origins, and implementing appropriate rate limiting.
- Do not use real learner personal data, sensitive assessments or consequential student records in a public demo without consent, purpose limitation and data-protection controls.
- Generated question content and inferred response labels may be incorrect or biased; do not use them for high-stakes decisions.
- Avoid exposing an internet-facing application until dependencies, secrets, access control, input validation, logging, backups and retention have been independently reviewed.

To report a suspected vulnerability, contact the repository maintainer privately through a channel they have designated. Do not include live credentials, personal records or exploit data in a public issue.
