# OWASP Top 10 Checklist (2021 baseline + 2025 direction)

A practical checklist to walk through every sprint diff. Each category has:
- What it is
- Concrete code / config checks
- Remediation patterns

---

## A01:2021 — Broken Access Control

### Checks
- [ ] Every endpoint checks authorization, not just authentication
- [ ] No IDOR: user can only access their own resources (check `tenantId` / `userId` filters on every query)
- [ ] Admin routes gated by role + MFA
- [ ] Force-browsing protection (no sensitive pages accessible without login)
- [ ] CORS is allow-list, not `*` in production
- [ ] No JWT without signature verification
- [ ] No "remember me" tokens that don't expire

### Fix Patterns
- Centralized authorization middleware
- Policy layer (Casbin, Oso, custom RBAC/ABAC)
- Row-Level Security in Postgres for multi-tenant data

---

## A02:2021 — Cryptographic Failures

### Checks
- [ ] TLS 1.2+ enforced (prefer 1.3); HSTS preload
- [ ] No hardcoded keys / secrets
- [ ] Strong algorithms: AES-256-GCM, ChaCha20-Poly1305; no MD5, SHA-1, DES, RC4
- [ ] Random via `crypto.getRandomValues` / `secrets` / `os.urandom`, not `Math.random()`
- [ ] Password hashing: Argon2id (preferred), bcrypt (acceptable), NOT SHA-256 alone
- [ ] Tokens have appropriate expiry (access ~15m, refresh rotated)
- [ ] PII encrypted at rest
- [ ] Secrets in vault, not in images or env-baked configs

### Fix Patterns
- `crypto` module for primitives (Node, Python, Go stdlib)
- Argon2id with memory cost 64MB+, parallelism 4+
- KMS / Vault for key management

---

## A03:2021 — Injection

### Checks
- [ ] All DB queries parameterized (no string concatenation of user input)
- [ ] OS commands: avoid or use `execFile` with args array, never `exec` with shell
- [ ] LDAP / XPath / NoSQL queries parameterized
- [ ] Template engines: auto-escape on; use `raw` / `safe` only with sanitized input
- [ ] JSON paths: validated schema
- [ ] CSV injection: prefix `=+-@` in exports

### Fix Patterns
- ORMs (Prisma, SQLAlchemy, Drizzle) enforce parameterization
- Input validation with Zod / Pydantic at boundary
- Output encoding (DOMPurify for HTML)

---

## A04:2021 — Insecure Design

### Checks
- [ ] Threat model exists for the feature (STRIDE)
- [ ] Abuse cases considered (what if this is used maliciously?)
- [ ] Rate limiting on auth + expensive + email/SMS endpoints
- [ ] Idempotency keys for payment / critical actions
- [ ] Business logic limits enforced server-side (never trust the client)

### Fix Patterns
- Security requirements in the spec, not bolted on
- Dedicated design review for auth, payment, privilege flows

---

## A05:2021 — Security Misconfiguration

### Checks
- [ ] Default credentials changed
- [ ] Error messages don't leak stack traces / internal paths to users
- [ ] Debug endpoints disabled in production
- [ ] Cloud bucket policies: no public unless intentional
- [ ] Security headers: CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy
- [ ] Docker: non-root user, minimal base image, no unused packages
- [ ] Kubernetes: NetworkPolicy, PodSecurityStandard, no hostPath mounts

### Fix Patterns
- `helmet` for Node, `Secure` middleware for Python
- IaC scanning (Checkov, tfsec)
- Baseline policy enforcement via OPA / Kyverno

---

## A06:2021 — Vulnerable and Outdated Components

### Checks
- [ ] SBOM generated and reviewed this sprint
- [ ] No dependencies with CRITICAL/HIGH CVE
- [ ] Lockfile committed (`package-lock.json`, `poetry.lock`, `go.sum`)
- [ ] EOL runtimes replaced (Node 16 EOL, Python 3.8 EOL, etc.)
- [ ] Automated updates via Dependabot / Renovate

### Fix Patterns
- Pin exact versions for production libraries
- Scheduled weekly scan + auto-PR for patch updates
- `npm audit --production`, `pip-audit`, `govulncheck`

---

## A07:2021 — Identification and Authentication Failures

### Checks
- [ ] MFA for admin and high-privilege accounts
- [ ] Strong password policy (min 12 chars, breach check via HIBP k-anonymity API)
- [ ] Account lockout / exponential backoff after failed logins
- [ ] Session: `HttpOnly`, `Secure`, `SameSite=Lax` or `Strict`
- [ ] Session rotation on privilege elevation
- [ ] Logout actually invalidates server-side session / refresh token
- [ ] No credentials over GET (querystring)

### Fix Patterns
- Trusted auth provider (Auth0, Clerk, Supabase Auth, Keycloak)
- Passkeys (WebAuthn) where possible

---

## A08:2021 — Software and Data Integrity Failures

### Checks
- [ ] CI/CD uses signed artifacts
- [ ] No unverified third-party code executed at runtime
- [ ] Auto-update mechanisms verify signature
- [ ] Webhooks verify signature (HMAC with shared secret)
- [ ] Serialization: safe libraries (no Java native `ObjectInputStream` on untrusted input, no `pickle` on untrusted data)

### Fix Patterns
- Sigstore / Cosign for artifact signing
- SLSA level targeting for critical services
- Integrity via Subresource Integrity on CDN scripts

---

## A09:2021 — Security Logging and Monitoring Failures

### Checks
- [ ] Auth events logged (success + failure)
- [ ] High-value actions logged (privilege change, data export, payment)
- [ ] Logs centralized (not only on local disk)
- [ ] Alerting on anomalies (10x normal 5xx, surge in 401/403)
- [ ] Logs do NOT contain passwords, tokens, PII
- [ ] Retention matches compliance (LGPD: minimize; SOC2: typically 1 year+)

### Fix Patterns
- Structured logging (JSON) with correlation IDs
- Log shipping to SIEM / Datadog / Grafana Loki
- Audit log separate from app log, append-only

---

## A10:2021 — Server-Side Request Forgery (SSRF)

### Checks
- [ ] User-provided URLs never passed directly to `fetch`/`http.request`
- [ ] Allow-list of outbound domains
- [ ] IMDS endpoint (`169.254.169.254`) blocked at egress
- [ ] DNS rebinding protection (resolve once, compare IP class)
- [ ] No `file://`, `gopher://`, `dict://` schemes accepted

### Fix Patterns
- URL validation + allow-list
- Outbound proxy with deny-list for private ranges (RFC 1918, IPv6 ULA)

---

## OWASP 2025 Direction (expected additions / elevations)

The next revision is expected to emphasize:

### Supply Chain (current A08, expected to split / elevate)

- SBOM generation + verification
- Dependency provenance
- Build reproducibility
- Signed artifacts end-to-end

See [supply-chain-security.md](supply-chain-security.md).

### Exceptional Conditions / Error Handling

- Unhandled exceptions revealing secrets
- Failure modes that fail-open instead of fail-closed
- Race conditions in privilege checks
- Panic / unwrap that crashes service mid-transaction

### LLM / AI-specific (OWASP LLM Top 10 tracks separately)

If the app uses an LLM:
- Prompt injection defense
- Output encoding when rendering LLM responses
- Rate-limit + cost cap per user
- Training data poisoning awareness for fine-tuned models
- Sensitive data exfiltration via prompts

See the OWASP Top 10 for LLM Applications for dedicated coverage.

---

## Walkthrough Protocol for a Sprint Diff

1. For each changed file, identify which categories could apply
2. Run SAST tools and cross-check manually
3. Note findings with file:line + category + CVSS + EPSS
4. For each finding, propose specific fix
5. Verify fix actually resolves (no cosmetic patches)
6. Re-scan after fix
7. Include walkthrough in the Security Gate Report
