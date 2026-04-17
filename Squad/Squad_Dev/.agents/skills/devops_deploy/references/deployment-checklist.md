# Deployment Checklist

Pre-deploy, deploy-time, and post-deploy checks by mode. Copy the right section
into your PR/runbook.

---

## Universal Pre-Deploy (every mode)

### Code & Tests
- [ ] All tests green (unit, integration, E2E for critical flows)
- [ ] Coverage maintained or improved
- [ ] Lint + type-check passing
- [ ] No TODOs tagged as "before deploy"

### Security
- [ ] Security Gate APPROVED for the sprint
- [ ] No CRITICAL/HIGH vulnerabilities in SBOM
- [ ] Secrets in vault, not in code or image
- [ ] Image signed (Cosign) if container-based

### Observability
- [ ] Logs structured (JSON) with correlation ID
- [ ] Metrics endpoint or agent configured
- [ ] Traces configured (OpenTelemetry)
- [ ] Error reporter (Sentry etc.) initialized
- [ ] Dashboards exist for this service

### Data
- [ ] Database backup within last 24h (or automated ongoing)
- [ ] Migrations forward-compatible (old app reads new schema)
- [ ] Seed/reference data updated
- [ ] No schema-breaking changes without migration plan

### Operations
- [ ] Rollback procedure documented AND rehearsed
- [ ] Runbook exists for known alerts
- [ ] On-call rotation confirmed
- [ ] Status page / comms channel ready
- [ ] Deploy window negotiated (avoid Friday/weekend)

---

## Deploy-Time

### Before cutting
- [ ] Announce deploy start in ops channel
- [ ] Pin on-call
- [ ] Start screen-share or log session if team-wide

### During
- [ ] Monitor error rate, latency p95, traffic in real time
- [ ] Canary stage passed smoke tests before expanding
- [ ] Database migration completed without locking errors

### After initial rollout
- [ ] No new error signatures
- [ ] Latency within SLO
- [ ] All pods/instances healthy
- [ ] Health check green from external monitor

---

## Post-Deploy

### First 30 minutes
- [ ] Active watching -- no multitasking
- [ ] Any alert triggered? Root-cause before standing down

### First 24 hours
- [ ] Error rate comparable to pre-deploy baseline
- [ ] No uptick in user-reported issues
- [ ] Background jobs completing at normal rate
- [ ] No data drift in key tables

### Documentation
- [ ] Deployment_Guide.md updated with new version + artifact hash
- [ ] Changelog marks version as released
- [ ] AI_CONTEXT.md updated with deploy date
- [ ] Any discovered gaps added to runbooks

---

## Mode-Specific

### PaaS (Vercel / Netlify / Fly)

- [ ] Env vars set per environment (never share prod keys in preview)
- [ ] Build command + output directory correct
- [ ] Custom domain + TLS propagated
- [ ] Preview deploys enabled for PR review

### Cloud Run (GCP)

- [ ] Min/max instances tuned to expected traffic
- [ ] Concurrency value matches workload
- [ ] Secrets from Secret Manager (not env vars)
- [ ] Service account has minimum required roles
- [ ] VPC connector if accessing private resources
- [ ] Allow-unauthenticated only for public endpoints

### AWS (ECS / Fargate / Lambda)

- [ ] Task role + Execution role separate
- [ ] ALB listener with HTTPS (HTTP redirect to HTTPS)
- [ ] Target group health check matches app readiness
- [ ] CloudWatch log group retention set
- [ ] Parameter Store / Secrets Manager referenced correctly
- [ ] Auto-scaling target tracking configured

### Kubernetes

- [ ] Resource requests + limits set (no "best effort")
- [ ] Readiness + liveness probes distinct and correct
- [ ] PodDisruptionBudget for HA workloads
- [ ] HPA configured with reasonable thresholds
- [ ] NetworkPolicy default-deny + explicit allows
- [ ] PodSecurityStandard restricted where possible
- [ ] PersistentVolume backup configured
- [ ] Ingress with TLS + rate limiting

### VPS / Docker Compose

- [ ] SSH key-only auth (no password)
- [ ] Non-root deploy user
- [ ] UFW / firewall configured
- [ ] Fail2ban or equivalent
- [ ] Automatic security updates enabled
- [ ] Reverse proxy (Caddy/Traefik/Nginx) with TLS
- [ ] Container runs as non-root
- [ ] Volume backups scheduled and tested

### Edge (Cloudflare Workers / Vercel Edge)

- [ ] Bundle size within platform limit
- [ ] No Node-only APIs relied upon
- [ ] KV / R2 / Durable Objects / D1 binding verified
- [ ] Custom domain + route configured
- [ ] Observability: Workers Analytics / Logflare / external

### Mobile (iOS App Store)

- [ ] Certificate + provisioning profile valid
- [ ] Privacy manifest + permission strings complete
- [ ] Screenshots + metadata final
- [ ] Demo account provided (if login required)
- [ ] Version + build number bumped
- [ ] TestFlight beta run for min 48h
- [ ] Staged release toggled in App Store Connect

### Mobile (Google Play)

- [ ] Upload key + app signing verified
- [ ] Data Safety form matches privacy policy
- [ ] Target SDK current requirement
- [ ] Staged rollout 1% → 5% → 20% → 50% → 100%
- [ ] Crashlytics + Play Console Vitals watched

---

## Emergency Rollback

- [ ] Decide: rollback vs fix-forward (< 30min to fix = fix-forward)
- [ ] Execute rollback via platform-appropriate command
- [ ] Verify metrics restored
- [ ] Announce rollback in ops channel
- [ ] Open incident ticket
- [ ] Post-mortem scheduled (blameless) within 48h
- [ ] Runbook updated if new failure mode discovered

---

## Deploy Smells (stop and reconsider)

- [ ] Skipping a gate "just this once"
- [ ] "We'll add tests after the deploy"
- [ ] "Rollback will be hard but unlikely"
- [ ] Secrets being rotated during deploy (do it separately)
- [ ] Running migrations after app cutover (should be before + forward-compatible)
- [ ] Missing sign-off from security or QA

Any of these = push back or escalate.
