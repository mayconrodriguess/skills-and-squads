---
name: devops-deploy
description: >
  Build, deploy e operações contínuas do projeto, do local ao production rollout.
  TRIGGERS: deploy, deployment, release, rollout, rollback, ci, cd, ci/cd,
  pipeline, github actions, gitlab ci, jenkins, circleci, docker, dockerfile,
  docker compose, kubernetes, k8s, helm, argocd, flux, terraform, pulumi,
  ansible, cloud run, aws, ecs, fargate, lambda, vercel, netlify, fly.io, railway,
  render, heroku, digitalocean, vps, ssh, nginx, caddy, traefik, let's encrypt,
  tls, certificate, monitoring, prometheus, grafana, datadog, sentry, logs,
  observability, slo, sli, canary, blue green, feature flag, release, smoke test,
  health check, readiness probe, liveness probe, autoscale, hpa, app store,
  play store, eas, fastlane.
---

# DevOps Deploy

Você transforma o código aprovado em `app_build/` em um sistema rodando, com
feedback operacional claro e segurança por default.

> "Automatize o repetível. Documente o excepcional. Nunca apresse mudanças em produção."

---

## 1. Project Structure Contract

| Folder | Purpose |
|---|---|
| `production_artifacts/Deployment_Guide.md` | Guia operacional (deploy, rollback, recovery) |
| `production_artifacts/docs/runbooks/` | Procedimentos para incidentes comuns |
| `production_artifacts/infra/` | IaC (Terraform, Pulumi, Cloud Formation) |
| `app_build/` | Aplicação a deployar |
| `app_build/Dockerfile` | Container definition |
| `app_build/docker-compose.yml` | Composição local |
| `.github/workflows/` ou `.gitlab-ci.yml` | Pipeline |
| `scripts/` | Bootstrap, migrations, smoke-test |
| `references/` | Platform notes, environment specifics |

---

## 2. Required Inputs

| Document | Required | Why |
|---|---|---|
| `production_artifacts/Solution_Architecture.md` | YES | Deployment topology |
| `production_artifacts/Tech_Stack_Rationale.md` | When present | Runtime choices |
| QA Report (PASS) | YES for prod | Não deploya com QA falhando |
| Security Gate Report (APPROVED) | YES for prod | Não deploya com gate bloqueado |
| Secrets inventory | YES | Conhecer TODOS os secrets antes de deploy |

---

## 3. Seleção do Modo de Deploy

Identifique o modo antes de qualquer ação:

| Modo | Gatilho |
|---|---|
| **Local** | Dev/teste, "roda aqui" |
| **PaaS** | Vercel, Netlify, Fly.io, Railway, Render |
| **Cloud Run (GCP)** | "Google Cloud", "Cloud Run", URL pública GCP |
| **AWS ECS / Fargate** | "AWS", container orquestrado |
| **Kubernetes** | "k8s", cluster existente, complexidade |
| **VPS/Docker** | "VPS", "servidor", Docker Compose |
| **Edge (Workers)** | Cloudflare, Vercel Edge, Deno Deploy |
| **Mobile Stores** | iOS App Store / Google Play |

---

## 4. Workflow Geral (qualquer modo)

### Fase 1 -- Discovery

1. Identificar stack em `app_build/`
2. Listar secrets necessários + onde vivem (vault, Secret Manager, GitHub Secrets)
3. Confirmar ambientes: dev / staging / prod
4. Validar que QA e Security Gate passaram (para prod)

### Fase 2 -- Build

5. Lint + type-check
6. Unit + integration tests
7. Build artifact (image, bundle, binary)
8. SBOM + scan da imagem (Trivy/Grype)
9. Assinar artifact (Cosign se container)

### Fase 3 -- Deploy Staging

10. Deploy em staging
11. Migrations executadas (forward-compatible)
12. Smoke test automatizado
13. QA spot-check manual se mudança grande

### Fase 4 -- Deploy Produção

14. Janela de deploy negociada (evitar sexta/fim de semana salvo emergência)
15. Deploy gradual (canary / staged / blue-green)
16. Monitor ativo por 15-30 min
17. Se métricas estáveis, expandir rollout
18. Se alarmes, rollback imediato

### Fase 5 -- Pós-Deploy

19. Atualizar `Deployment_Guide.md` com versão + artifact hash
20. Atualizar changelog
21. Comunicar stakeholders
22. Arquivar logs de deploy por compliance

---

## 5. Modo Local

### Objetivo
Rodar de forma segura e reproduzível.

### Fluxo
1. Detectar stack (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`)
2. Listar variáveis de ambiente em falta a partir de `.env.example`
3. Instalar deps (`npm ci`, `pip install -e .`, `cargo build`, `go mod download`)
4. Executar migrations/seeds se aplicável
5. Build se stack precisa (TS, Next, React, Svelte, Flutter)
6. Iniciar app + health check na porta esperada

### Output
```
[OK] Aplicação rodando em: http://localhost:3000
Stack: Next.js 15 + PostgreSQL
Para parar: Ctrl+C
```

---

## 6. Modo PaaS (Vercel / Netlify / Fly / Railway / Render)

PaaS é o caminho mais rápido para ship quando cabe no modelo deles.

### Vercel
- `vercel.json` para configuração avançada
- Env vars por ambiente (Preview / Production)
- Preview Deployments em PRs = QA manual fácil
- Vercel Analytics + Speed Insights

### Netlify
- `netlify.toml` com redirects, headers, functions
- Edge Functions (Deno runtime)

### Fly.io
- `fly.toml` define a app
- Rollouts com `fly deploy --strategy canary`
- Postgres gerenciado via `fly postgres`
- Multi-região via `fly scale count` por região

### Railway / Render
- Zero-config para stacks comuns
- Auto-deploy no push
- Boa para MVPs e apps internos

---

## 7. Modo Cloud Run (GCP)

### Pré-requisitos
- [ ] `gcloud` autenticado (`gcloud auth login`)
- [ ] Project ID configurado
- [ ] APIs habilitadas: Cloud Run, Artifact Registry, Cloud Build
- [ ] Secrets em Secret Manager (NUNCA em env vars da imagem)
- [ ] Imagem non-root, minimalista (distroless/alpine)

### Deploy
```bash
gcloud run deploy myapp \
  --source . \
  --region us-central1 \
  --set-secrets=DATABASE_URL=database-url:latest \
  --min-instances=0 --max-instances=50 \
  --cpu=1 --memory=512Mi \
  --allow-unauthenticated   # remover para serviços internos
```

### Configurações importantes
- `--concurrency=80` (ajustar ao workload)
- `--timeout=60s` (maior para jobs assíncronos)
- `--cpu-boost` para melhor cold start
- `--execution-environment=gen2` (default moderno)
- VPC connector se precisa acessar recursos privados

### Output
```
[OK] Deploy concluído
URL: https://myapp-xxxxx-uc.a.run.app
Região: us-central1
Revisão: myapp-00042-abc
Hash: sha256:...
```

---

## 8. Modo AWS (ECS Fargate / Lambda)

### ECS Fargate
- Task definition com limites de CPU/memória
- ALB na frente para TLS + routing
- CloudWatch Logs + Container Insights
- IAM roles mínimos (Task role != Execution role)
- Secrets via AWS Secrets Manager ou SSM Parameter Store

### Lambda (serverless)
- Handler por função, bundled pequeno
- Cold start: provisioned concurrency se crítico
- API Gateway ou Lambda URL na frente
- PowerTools (logger, tracer, metrics) para observability

---

## 9. Modo Kubernetes

Apenas se o time tem experiência operacional. Complexidade não paga para <5 serviços.

### Essenciais
- Namespace por ambiente (dev/staging/prod) ou por tenant
- Deployment + Service + Ingress (ou Gateway API)
- HPA (Horizontal Pod Autoscaler) em CPU e custom metrics
- PodDisruptionBudget para alta disponibilidade
- NetworkPolicy (default-deny)
- PodSecurityStandard restricted
- Liveness + readiness probes SEMPRE
- Resource requests + limits em todo container

### GitOps
- ArgoCD ou Flux
- App-of-apps para orquestrar ambientes
- Helm ou Kustomize para templating
- Secrets via Sealed Secrets, External Secrets Operator, ou SOPS

---

## 10. Modo VPS / Docker Compose

### Fluxo
1. Acesso SSH com chave (nunca senha)
2. Usuário não-root com sudo explícito
3. Build da imagem localmente ou em CI
4. Push para registry (GHCR, Docker Hub, ECR)
5. `docker compose pull && docker compose up -d`
6. Verificar health + logs
7. TLS via Caddy/Traefik (auto Let's Encrypt) ou Nginx + Certbot

### Checklist
- [ ] Firewall (UFW): apenas 22, 80, 443
- [ ] Fail2ban para SSH
- [ ] Unattended-upgrades
- [ ] Backup do banco ANTES do deploy
- [ ] Reverse proxy com rate limiting

---

## 11. Modo Mobile (Stores)

### Android (Google Play)
```bash
# React Native (Expo)
eas build --platform android --profile production
eas submit --platform android

# Flutter
flutter build appbundle --release
# upload via Google Play Console ou fastlane

# Native
./gradlew bundleRelease
fastlane supply
```

### iOS (App Store)
```bash
# Expo
eas build --platform ios --profile production
eas submit --platform ios

# Flutter
flutter build ipa --release
# upload via Transporter ou fastlane

# Native
xcodebuild archive ...
fastlane deliver
```

Ver o skill `mobile_developer` para prep de store completa.

---

## 12. CI/CD com Security Gates

Todo pipeline de produção deve incluir:

```yaml
Pipeline:
  1. Install deps (cache)
  2. Lint + type-check
  3. Unit + Integration tests
  4. SAST (Semgrep / CodeQL)         # security gate
  5. SCA (npm audit / pip-audit)     # security gate
  6. Secrets scan (gitleaks)         # security gate
  7. Build artifact
  8. SBOM (CycloneDX)
  9. Container scan (Trivy)          # security gate
  10. Sign artifact (Cosign)
  11. Deploy staging
  12. Smoke test
  13. Deploy production (canary/staged)  # manual approval
  14. Post-deploy smoke + monitor
```

Regra: qualquer falha em gate = pipeline para.

---

## 13. Deployment Strategies

| Estratégia | Descrição | Quando |
|---|---|---|
| **Recreate** | Stop old, start new | Dev; downtime aceitável |
| **Rolling** | Substitui pods gradualmente | Default k8s; simples |
| **Blue-Green** | Ambiente paralelo, switch de tráfego | Zero downtime, rollback instantâneo |
| **Canary** | X% tráfego para nova versão, monitor, expande | Mudanças arriscadas |
| **Shadow** | Nova versão recebe tráfego espelhado sem responder | Testar performance antes de cutover |
| **Feature flag** | Deploy sem ativar; ativa para % de usuários | Desacopla deploy de release |

**Regra**: prod em staged (canary/blue-green). Feature flags sobre tudo que pode dar errado.

---

## 14. Observability (ship from day one)

- **Logs**: JSON estruturado, correlation IDs, ship para Datadog/Loki/CloudWatch
- **Métricas**: RED (Rate, Errors, Duration) por serviço; USE (Utilization, Saturation, Errors) por recurso
- **Traces**: OpenTelemetry ponta a ponta
- **Erros**: Sentry, Bugsnag, Rollbar
- **Uptime**: Better Stack, StatusCake, Pingdom
- **Dashboards**: 1 por serviço, foco em SLIs

### SLOs mínimos
- Availability: 99.9% ou mais, medido em janela
- Latency: p95 < SLO definido
- Error rate: < 1% (depende do domínio)

### Alertas
- Baseados em SLO burn rate (não em thresholds arbitrários)
- On-call rotation clara
- Runbook vinculado a cada alerta

---

## 15. Protocolo de Segurança (Produção)

### Sempre
- Confirmar antes de comandos destrutivos (drop, delete, truncate)
- Backup antes de mudanças de schema
- Testar em staging idêntico a prod
- Monitorar 15-30 min pós-deploy
- Plano de rollback documentado ANTES do deploy

### Nunca
- Deploy sem aprovação do `@security-specialist`
- Deploy às sextas/fins de semana (salvo emergência)
- `--force`, `-f`, `--no-verify` sem justificativa explícita
- Credenciais em env vars da imagem
- Skip de CI gates "só essa vez"

---

## 16. Rollback de Emergência

```
1. AVALIAR: Qual sintoma? Logs, métricas, traces?
2. DECIDIR: Rollback vs Fix-forward?
   - Rollback se: regressão clara, usuários afetados, fix > 30min
   - Fix-forward se: dado já comprometido, rollback não resolve
3. EXECUTAR ROLLBACK:
   - Cloud Run: volta para revisão anterior (1 comando)
   - Kubernetes: kubectl rollout undo
   - PaaS: redeploy do commit anterior
   - Feature flag: desativar flag
4. CONFIRMAR: métricas estabilizaram?
5. COMUNICAR: stakeholders + usuários (status page)
6. POST-MORTEM: blameless, em 48h
```

---

## 17. Quality Bar

Antes de liberar deploy de produção:

- [ ] QA Report PASS do sprint
- [ ] Security Gate APPROVED
- [ ] Secrets em vault, não em código
- [ ] Migrations forward-compatible (app velha roda com schema novo)
- [ ] Health + readiness probes configurados
- [ ] Logs estruturados + correlation IDs
- [ ] Alertas ligados aos SLOs
- [ ] Staging idêntico a prod testado
- [ ] Rollback testado (não só documentado)
- [ ] Runbook atualizado para alertas conhecidos
- [ ] Janela de deploy negociada
- [ ] On-call notificado

Ver [references/deployment-checklist.md](references/deployment-checklist.md)
para checklist expandido por modo.

---

## 18. Bundled Reference

| File | Contents |
|---|---|
| [references/deployment-checklist.md](references/deployment-checklist.md) | Pre/during/post deploy por modo |

---

## 19. Deliverables

Todo deploy produz:

1. Artifact hash + URL em `production_artifacts/Deployment_Guide.md`
2. Changelog atualizado com versão shipped
3. Dashboards + alertas verificados ativos
4. Runbook atualizado se nova falha-pattern descoberta
5. Atualização de `production_artifacts/memory/AI_CONTEXT.md` com versão + data
