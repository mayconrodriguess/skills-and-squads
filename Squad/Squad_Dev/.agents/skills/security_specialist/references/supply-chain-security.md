# Supply Chain Security

Dependency hygiene, SBOM, signing, SLSA. Supply chain attacks have moved from
theoretical to weekly occurrence (event-stream, colors.js, ua-parser-js,
xz-utils, etc.). Assume every new dependency is a threat vector until proven
otherwise.

---

## 1. The Threat Surface

| Attack | Example |
|---|---|
| Typosquatting | `lod4sh` instead of `lodash` |
| Dependency confusion | Private name published publicly with higher version |
| Compromised maintainer | Legitimate package pushes a malicious release |
| Malicious install scripts | `postinstall` runs arbitrary code |
| Backdoored build tools | xz-utils 5.6 (2024) |
| Compromised CI secrets | Attacker injects code via pipeline |
| Unverified CDN assets | Modified JS served from third party |

Your job: reduce every surface to the minimum, monitor the rest.

---

## 2. SBOM (Software Bill of Materials)

### Why
A machine-readable inventory of every dependency (direct + transitive). Lets
you answer "Am I affected by CVE-X?" in seconds instead of hours.

### Format
- **CycloneDX** (OWASP-maintained, JSON or XML)
- **SPDX** (Linux Foundation)

### How to Generate

Node:
```bash
npx @cyclonedx/cyclonedx-npm --output-file sbom.cdx.json
```

Python:
```bash
pip install cyclonedx-bom
cyclonedx-py -o sbom.cdx.json
```

Go:
```bash
cyclonedx-gomod mod -json -output sbom.cdx.json
```

Container images:
```bash
syft packages docker:myapp:latest -o cyclonedx-json > sbom.cdx.json
```

### Where to Store
`production_artifacts/security/sbom-<version>-<date>.cdx.json`

Commit every release's SBOM. Query with `grype sbom:sbom.cdx.json` or upload
to Dependency-Track for continuous monitoring.

---

## 3. Dependency Pinning

### Rules

| Level | Approach |
|---|---|
| Direct deps | Pin minor+patch range (`^1.2.3`) |
| Transitive deps | Frozen by lockfile |
| Production builds | Use `--frozen-lockfile` / `npm ci` / `pip install --require-hashes` |
| Critical prod runtime | Pin exact version; upgrade deliberately |

### Files That MUST Be Committed

- `package-lock.json` / `pnpm-lock.yaml` / `yarn.lock`
- `poetry.lock` / `Pipfile.lock` / `requirements.txt` with hashes
- `Cargo.lock`
- `go.sum`
- `composer.lock`

If lockfile is in `.gitignore`, that's a finding.

---

## 4. Pre-Install Scripts

npm packages can run `preinstall`, `install`, `postinstall` scripts. These have
been used to exfiltrate secrets.

### Mitigations
- `npm ci --ignore-scripts` where possible
- Review new dependencies for suspicious scripts
- Use `pnpm` with `onlyBuiltDependencies` allow-list
- CI: run install in an isolated container

---

## 5. Vulnerability Scanning

### Tools

| Tool | Stack | Notes |
|---|---|---|
| `npm audit` / `pnpm audit` | Node | Built-in |
| `pip-audit` | Python | OSS, uses PyPI + OSV |
| `govulncheck` | Go | Official, reachability-aware |
| `cargo audit` | Rust | Uses RustSec DB |
| `Trivy` | Multi / container | OSS, very fast |
| `Grype` | Multi / SBOM | Pair with syft |
| `Snyk` | Multi | Commercial, good UI |
| `osv-scanner` | Multi | Google OSS, OSV DB |
| `Dependabot` | GitHub | Auto PR for updates |
| `Renovate` | Multi | More configurable than Dependabot |

### Frequency
- Pre-commit hook: warn on known CVEs in changed deps
- CI on every PR: block on CRITICAL
- Nightly full scan on main: surfaces newly disclosed CVEs in existing deps

---

## 6. CVSS + EPSS Combined Prioritization

CVSS alone over-prioritizes theoretical severity. Combine with EPSS (Exploit
Prediction Scoring System) to prioritize what attackers actually use.

| CVSS | EPSS | Priority |
|---|---|---|
| >= 9.0 | > 0.5 | PATCH NOW |
| >= 9.0 | < 0.1 | Patch this sprint |
| 7.0-8.9 | > 0.5 | Patch this sprint |
| 7.0-8.9 | < 0.1 | Next sprint |
| < 7.0 | > 0.5 | Next sprint |
| < 7.0 | < 0.1 | Backlog |

EPSS data: [https://www.first.org/epss/](https://www.first.org/epss/)

---

## 7. Artifact Signing (Sigstore / Cosign)

Sigstore provides free, transparent, keyless signing for container images and
generic artifacts.

```bash
# Sign
cosign sign --yes myregistry/myapp:1.2.3

# Verify
cosign verify --certificate-identity-regexp '.*@yourorg\.com$' \
              --certificate-oidc-issuer https://token.actions.githubusercontent.com \
              myregistry/myapp:1.2.3
```

Verify signatures at deploy time -- don't just sign. Unverified signatures are
decoration.

---

## 8. SLSA (Supply-chain Levels for Software Artifacts)

A maturity framework:

| Level | What |
|---|---|
| SLSA 1 | Build is scripted + provenance generated |
| SLSA 2 | Version-controlled source + hosted build + signed provenance |
| SLSA 3 | Non-falsifiable provenance + isolated builds |
| SLSA 4 | Two-person review + hermetic builds + reproducible |

GitHub Actions + `actions/attest-build-provenance` gets you SLSA 3 with minimal
effort.

Target SLSA 3 for production artifacts of non-trivial services.

---

## 9. Container Image Hygiene

- Base from digest, not tag: `FROM node@sha256:abc123...`
- Minimal base: `distroless`, `alpine`, `scratch` where possible
- Multi-stage build: build artifacts on one image, copy to minimal runtime
- Non-root user (`USER node`)
- No sensitive files baked in (check final layer)
- Scan every image in CI (Trivy / Grype)
- Sign every image (Cosign)
- Store SBOM as an attestation alongside the image

---

## 10. Dependency Review Checklist (New Dep)

Before adding any new dependency:

- [ ] Is it maintained? (commit activity last 6 months)
- [ ] Is it widely used? (downloads, dependents)
- [ ] Does it have tests? (coverage > 0?)
- [ ] Does it have suspicious install scripts?
- [ ] Does it have network calls at import time?
- [ ] License compatible? (MIT, Apache, BSD usually safe; GPL may conflict)
- [ ] Alternatives considered?
- [ ] Will someone on the team own its upgrade cycle?

Document the review in the PR description when adding a significant dep.

---

## 11. Secrets Hygiene in Supply Chain

- CI secrets scoped to minimum (per-env, per-job)
- OIDC federation instead of long-lived access keys (AWS, GCP, Azure all support it)
- Rotate tokens quarterly or on any suspicion
- No secrets in logs, even for debugging
- `.env.example` has placeholders, not real values

---

## 12. Incident Playbook: Compromised Dependency

If a dep you use is reported as compromised:

1. **Immediately** check if your production image includes the malicious version
2. If yes: rotate all secrets that could have been exposed
3. Pin to a known-good prior version
4. Rebuild + redeploy
5. Audit logs for unusual behavior during exposure window
6. Disclose internally (and publicly if user data may have been touched)
7. Post-mortem: why did the bad version pass our gate?

---

## 13. Quality Bar

- [ ] SBOM generated + committed for the release
- [ ] No CRITICAL/HIGH CVEs in runtime deps (or documented waiver)
- [ ] Lockfile committed and used in CI
- [ ] New deps reviewed (Section 10 checklist)
- [ ] Images signed (Cosign) and signatures verified at deploy
- [ ] SBOM + provenance attached to release artifacts
- [ ] Dependabot / Renovate active with auto-merge for patch
- [ ] CI uses `--ignore-scripts` or reviewed-scripts allow-list
