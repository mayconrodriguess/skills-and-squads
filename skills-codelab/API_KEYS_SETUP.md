# 🔑 Configuração de Chaves API — Skills Codelab

> Este arquivo explica como configurar todas as chaves de API e credenciais necessárias para o funcionamento completo do pipeline Autonomous AI Developer.

---

## Visão Geral

O pipeline utiliza diversas APIs e serviços externos. Nenhuma chave deve ser commitada no código — todas devem ser configuradas via **variáveis de ambiente** ou **arquivo `.env`**.

---

## Configuração Rápida

### 1. Copie o template de variáveis de ambiente

```bash
cp .env.example .env
```

### 2. Preencha as chaves no arquivo `.env`

Abra o `.env` e preencha os valores conforme as instruções abaixo.

### 3. Nunca commite o arquivo `.env`

Verifique que o `.gitignore` contém:
```
.env
.env.local
.env.production
*.key
*.pem
```

---

## Chaves Necessárias por Serviço

### 🤖 Antigravity IDE (Gemini AI)

O Antigravity usa o Gemini como modelo de IA. A autenticação é gerenciada pelo próprio IDE — **não é necessário configurar uma API key separada**. Basta estar logado no Antigravity com sua conta Google.

Se você estiver usando o Gemini API diretamente (fora do Antigravity):

| Variável | Descrição | Como Obter |
|:---|:---|:---|
| `GEMINI_API_KEY` | Chave da API Google Gemini | [Google AI Studio](https://aistudio.google.com/apikey) → Criar chave API |

```env
GEMINI_API_KEY=your-gemini-api-key-here
```

---

### ☁️ Google Cloud (Cloud Run Deploy)

Necessário apenas se você for usar a skill `deploy_cloud_run.md` para deploy em produção.

| Variável | Descrição | Como Obter |
|:---|:---|:---|
| `GOOGLE_CLOUD_PROJECT` | ID do projeto GCP | [Console GCP](https://console.cloud.google.com) → Selecione ou crie um projeto |
| `GOOGLE_APPLICATION_CREDENTIALS` | Caminho para o arquivo de service account JSON | Console GCP → IAM → Service Accounts → Criar chave |

**Setup:**
```bash
# Login no gcloud CLI
gcloud auth login

# Definir projeto
gcloud config set project YOUR_PROJECT_ID

# Habilitar Cloud Run API
gcloud services enable run.googleapis.com

# (Opcional) Criar service account para CI/CD
gcloud iam service-accounts create deployer \
  --display-name="Cloud Run Deployer"
```

```env
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GOOGLE_APPLICATION_CREDENTIALS=./credentials/service-account.json
```

---

### 📱 Publicação Mobile (Google Play + Apple)

Necessário apenas se você for usar a skill `mobile_developer.md` para publicar nas stores.

#### Google Play Store

| Variável | Descrição | Como Obter |
|:---|:---|:---|
| `GOOGLE_PLAY_SERVICE_ACCOUNT_KEY` | Caminho para JSON da service account do Play Console | [Play Console](https://play.google.com/console) → Setup → API access → Create service account |

```env
GOOGLE_PLAY_SERVICE_ACCOUNT_KEY=./credentials/google-play-key.json
```

**Setup:**
1. Acesse o [Google Play Console](https://play.google.com/console)
2. Vá em **Setup → API access**
3. Crie uma **Service Account** com permissão de "Release Manager"
4. Baixe o arquivo JSON e salve em `credentials/google-play-key.json`

#### Apple App Store

| Variável | Descrição | Como Obter |
|:---|:---|:---|
| `APPLE_ID` | Seu Apple ID (email) | Sua conta Apple Developer |
| `APPLE_APP_SPECIFIC_PASSWORD` | Senha específica para apps | [appleid.apple.com](https://appleid.apple.com) → Sign-in & Security → App-Specific Passwords |
| `ASC_APP_ID` | ID do app no App Store Connect | [App Store Connect](https://appstoreconnect.apple.com) → App → General Information |
| `APPLE_TEAM_ID` | Team ID da sua conta Developer | [Developer Account](https://developer.apple.com/account) → Membership |

```env
APPLE_ID=your-apple-id@email.com
APPLE_APP_SPECIFIC_PASSWORD=xxxx-xxxx-xxxx-xxxx
ASC_APP_ID=1234567890
APPLE_TEAM_ID=ABCDE12345
```

---

### 🎨 Ferramentas Criativas (AI Page Designer)

#### Google Whisk (Geração de Imagens)

| Variável | Descrição | Como Obter |
|:---|:---|:---|
| `WHISK_API_KEY` | Chave API do Google Whisk | [labs.google/whisk](https://labs.google/whisk) — verificar disponibilidade da API |

```env
WHISK_API_KEY=your-whisk-api-key-here
```

> **Nota:** Google Whisk pode ser usado diretamente via interface web sem API key. A variável é necessária apenas para integração automatizada via MCP Stitch.

#### Google Flow (Geração de Vídeos)

| Variável | Descrição | Como Obter |
|:---|:---|:---|
| `FLOW_API_KEY` | Chave API do Google Flow | [labs.google/flow](https://labs.google/flow) — verificar disponibilidade da API |

```env
FLOW_API_KEY=your-flow-api-key-here
```

> **Nota:** Mesma situação do Whisk — uso manual via web não requer key.

#### MCP Stitch (Orquestração)

| Variável | Descrição | Como Obter |
|:---|:---|:---|
| `MCP_STITCH_ENDPOINT` | URL do endpoint MCP Stitch | Conforme configuração do seu servidor MCP |
| `MCP_STITCH_TOKEN` | Token de autenticação | Gerado na configuração do MCP |

```env
MCP_STITCH_ENDPOINT=http://localhost:3001/mcp
MCP_STITCH_TOKEN=your-mcp-token-here
```

---

### 🗄️ Banco de Dados

#### PostgreSQL (Local via Docker)

Não requer API key. Configuração via variáveis de ambiente:

```env
DATABASE_URL=postgresql://app:your-secure-password@localhost:5432/appdb
DB_POOL_MIN=2
DB_POOL_MAX=10
```

#### Neon (Serverless PostgreSQL)

| Variável | Descrição | Como Obter |
|:---|:---|:---|
| `DATABASE_URL` | Connection string do Neon | [neon.tech](https://neon.tech) → Create project → Connection string |

```env
DATABASE_URL=postgresql://user:pass@ep-xxx.region.neon.tech/dbname?sslmode=require
```

#### Turso (Edge SQLite)

| Variável | Descrição | Como Obter |
|:---|:---|:---|
| `TURSO_DATABASE_URL` | URL do banco Turso | `turso db create appdb` → `turso db show appdb --url` |
| `TURSO_AUTH_TOKEN` | Token de autenticação | `turso db tokens create appdb` |

```env
TURSO_DATABASE_URL=libsql://your-db-name.turso.io
TURSO_AUTH_TOKEN=your-turso-token-here
```

#### Supabase

| Variável | Descrição | Como Obter |
|:---|:---|:---|
| `SUPABASE_URL` | URL do projeto | [supabase.com](https://supabase.com) → Project → Settings → API |
| `SUPABASE_ANON_KEY` | Chave pública (anon) | Mesma página |
| `SUPABASE_SERVICE_ROLE_KEY` | Chave privada (server-side only) | Mesma página |

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...
```

#### Redis

Não requer API key para local. Para Upstash (serverless Redis):

| Variável | Descrição | Como Obter |
|:---|:---|:---|
| `REDIS_URL` | URL de conexão | [upstash.com](https://upstash.com) → Create database → REST URL |

```env
# Local
REDIS_URL=redis://localhost:6379

# Upstash (serverless)
REDIS_URL=rediss://default:xxxxx@us1-xxx.upstash.io:6379
```

---

### 🚀 Expo / EAS (React Native Mobile)

| Variável | Descrição | Como Obter |
|:---|:---|:---|
| `EXPO_TOKEN` | Token de acesso ao EAS | [expo.dev](https://expo.dev) → Account Settings → Access Tokens → Create |

```env
EXPO_TOKEN=your-expo-token-here
```

**Setup:**
```bash
npm install -g eas-cli
eas login
eas build:configure
```

---

## Template `.env.example`

Copie este conteúdo para um arquivo `.env.example` na raiz do projeto:

```env
# ============================================
# 🔑 API Keys & Credentials
# ============================================
# Copy this file to .env and fill in your values
# NEVER commit .env to version control!
# ============================================

# --- Google Gemini (if using outside Antigravity) ---
# GEMINI_API_KEY=

# --- Google Cloud (Cloud Run deploy) ---
# GOOGLE_CLOUD_PROJECT=
# GOOGLE_APPLICATION_CREDENTIALS=./credentials/service-account.json

# --- Database ---
DATABASE_URL=postgresql://app:password@localhost:5432/appdb
# DATABASE_URL=file:./dev.db
# TURSO_DATABASE_URL=
# TURSO_AUTH_TOKEN=
# SUPABASE_URL=
# SUPABASE_ANON_KEY=
# SUPABASE_SERVICE_ROLE_KEY=

# --- Redis ---
REDIS_URL=redis://localhost:6379

# --- Database Pool ---
DB_POOL_MIN=2
DB_POOL_MAX=10

# --- Mobile: Expo / EAS ---
# EXPO_TOKEN=

# --- Mobile: Google Play Store ---
# GOOGLE_PLAY_SERVICE_ACCOUNT_KEY=./credentials/google-play-key.json

# --- Mobile: Apple App Store ---
# APPLE_ID=
# APPLE_APP_SPECIFIC_PASSWORD=
# ASC_APP_ID=
# APPLE_TEAM_ID=

# --- Creative Tools (AI Page Designer) ---
# WHISK_API_KEY=
# FLOW_API_KEY=
# MCP_STITCH_ENDPOINT=http://localhost:3001/mcp
# MCP_STITCH_TOKEN=

# --- App Config ---
NODE_ENV=development
PORT=3000
```

---

## Segurança

| Regra | Descrição |
|:---|:---|
| Nunca commite `.env` | Sempre no `.gitignore` |
| Use `.env.example` | Template sem valores reais para documentação |
| Rotacione chaves | Troque periodicamente, especialmente após vazamentos |
| Princípio do menor privilégio | Cada chave deve ter apenas as permissões necessárias |
| Ambientes separados | Use chaves diferentes para dev, staging e production |
| Secrets em CI/CD | Use GitHub Secrets, Doppler, ou Vault — nunca variáveis em código |

---

## Checklist de Setup

- [ ] Arquivo `.env` criado a partir de `.env.example`
- [ ] `.env` adicionado ao `.gitignore`
- [ ] Pasta `credentials/` adicionada ao `.gitignore`
- [ ] Chaves do banco de dados configuradas
- [ ] (Se mobile) Expo token configurado
- [ ] (Se mobile) Google Play service account configurada
- [ ] (Se mobile) Apple credentials configuradas
- [ ] (Se Cloud Run) gcloud CLI autenticado
- [ ] (Se Page Designer) Ferramentas criativas configuradas (se usando via API)

---

> **Dúvidas?** Se você não sabe qual chave precisa, rode `/startcycle` com sua ideia — o Solution Architect vai definir quais serviços são necessários e este guia indica exatamente quais chaves configurar.
