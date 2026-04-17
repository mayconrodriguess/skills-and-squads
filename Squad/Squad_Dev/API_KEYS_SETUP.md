# API Keys & Environment Setup

> ⚠️ **NUNCA** commitar este arquivo com valores reais preenchidos.
> Use `.env` local e adicione ao `.gitignore`.

---

## Variáveis de Ambiente Necessárias

Crie um arquivo `.env` na raiz de `app_build/` com as variáveis abaixo:

```env
# ============================================
# LLM / AI
# ============================================
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
GEMINI_API_KEY=

# ============================================
# Banco de Dados
# ============================================
DATABASE_URL=
POSTGRES_USER=
POSTGRES_PASSWORD=
POSTGRES_DB=

# ============================================
# Autenticação
# ============================================
JWT_SECRET=
JWT_EXPIRES_IN=7d
SESSION_SECRET=

# ============================================
# Cloud / Deploy
# ============================================
GCP_PROJECT_ID=
GCP_REGION=us-central1
CLOUD_RUN_SERVICE_NAME=

# ============================================
# Serviços Externos (adicionar conforme necessário)
# ============================================
SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASSWORD=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

# ============================================
# Configurações da Aplicação
# ============================================
NODE_ENV=development
PORT=3000
APP_URL=http://localhost:3000
LOG_LEVEL=debug
```

---

## Onde Cada Serviço Usa as Keys

| Variável | Usado por | Como obter |
|----------|-----------|------------|
| `DATABASE_URL` | `@database-specialist`, `@backend-specialist` | [Neon](https://neon.tech) / [Supabase](https://supabase.com) / local |
| `JWT_SECRET` | `@backend-specialist` | Gerar: `openssl rand -base64 32` |
| `GCP_PROJECT_ID` | `@devops-engineer` | [Google Cloud Console](https://console.cloud.google.com) |

---

## Segredos em Produção

Em produção, use **sempre** um secrets manager:

- **Google Cloud Run** → Secret Manager: `gcloud secrets create MY_SECRET --data-file=.env`
- **Docker/VPS** → Docker Secrets ou `.env` fora do repositório
- **Vercel/Railway** → Dashboard de variáveis de ambiente da plataforma

**Nunca:**
- ❌ Commitar `.env` com valores reais
- ❌ Hardcodar keys no código
- ❌ Deixar keys em comentários
- ❌ Compartilhar keys em mensagens/chats

---

## Setup Inicial (Checklist)

- [ ] Copiar este arquivo como referência
- [ ] Criar `app_build/.env` (não versionado)
- [ ] Preencher variáveis necessárias para o projeto
- [ ] Adicionar `app_build/.env` ao `.gitignore`
- [ ] Configurar CI/CD com secrets manager
