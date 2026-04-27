# Segundo Cérebro com IA — Procedimento Completo

> **Este documento é executável.** Foi escrito para ser seguido por humanos OU por uma IA agente (Claude, GPT, Gemini, etc.) com acesso a terminal.
>
> **Objetivo final:** qualquer IA com suporte a MCP consegue ler, buscar, criar, editar e gerenciar notas Obsidian autonomamente.

---

## Arquitetura

```
Vault Obsidian (.md no disco/OneDrive)
        │
        ▼
Plugin "Local REST API"  ──►  HTTP em 127.0.0.1:27123 (auth via API key)
        │
        ▼
Servidor MCP "obsidian-mcp-server" (cyanheads, via npx)
        │
        ├──► Claude Desktop
        ├──► Claude Code (CLI)
        ├──► VS Code Copilot Agent
        ├──► Cursor
        └──► Qualquer cliente MCP-compatível
```

**Capacidades expostas:** ler nota, criar nota, editar nota, append, buscar (texto/regex/Dataview), gerenciar tags, manipular frontmatter, listar pastas, mover/renomear arquivos.

---

## Pré-requisitos

| Item | Como verificar | Como instalar se faltar |
|------|----------------|--------------------------|
| Obsidian | Abrir o app | https://obsidian.md |
| Node.js 18+ | `node --version` | https://nodejs.org (LTS) |
| Cliente MCP | Claude Desktop / VS Code 1.99+ / Cursor | site oficial de cada um |

---

## PARTE 1 — Plugin Local REST API no Obsidian

### Instalação automática (para IA executar)

```powershell
# Variáveis (ajuste o $vault para o seu caminho)
$vault = "C:\Users\maycon\OneDrive\01_OBSIDIAN"
$pluginDir = "$vault\.obsidian\plugins\obsidian-local-rest-api"

# Gerar API key segura (64 hex)
$apiKey = -join ((1..32) | ForEach-Object { '{0:x2}' -f (Get-Random -Max 256) })

# Baixar plugin
New-Item -ItemType Directory -Force -Path $pluginDir | Out-Null
$base = "https://github.com/coddingtonbear/obsidian-local-rest-api/releases/latest/download"
Invoke-WebRequest "$base/main.json" -OutFile "$pluginDir\manifest.json" -UseBasicParsing
Invoke-WebRequest "$base/manifest.json" -OutFile "$pluginDir\manifest.json" -UseBasicParsing
Invoke-WebRequest "$base/main.js" -OutFile "$pluginDir\main.js" -UseBasicParsing

# Configurar plugin (HTTP forçado)
@"
{
  "apiKey": "$apiKey",
  "crypto": {},
  "enableInsecureServer": true,
  "insecurePort": 27123,
  "enableSecureServer": false,
  "bindingHost": "127.0.0.1"
}
"@ | Set-Content "$pluginDir\data.json" -Encoding utf8

# Habilitar plugin no Obsidian
$cpFile = "$vault\.obsidian\community-plugins.json"
$cp = if (Test-Path $cpFile) { Get-Content $cpFile -Raw | ConvertFrom-Json } else { @() }
if ($cp -notcontains "obsidian-local-rest-api") {
    $cp = @($cp) + "obsidian-local-rest-api"
    $cp | ConvertTo-Json | Set-Content $cpFile -Encoding utf8
}

Write-Host "API Key gerada: $apiKey"
Write-Host "Reinicie o Obsidian: taskkill /F /IM Obsidian.exe /T ; depois abra novamente"
```

### Validar (após reiniciar Obsidian)

```bash
curl -s http://127.0.0.1:27123/ -H "Authorization: Bearer SUA_API_KEY"
# Esperado: {"status":"OK","authenticated":true,...}
```

### Lições aprendidas (importantes)

1. **Campos do `data.json` NÃO seguem nomes da UI.** Use exatamente: `enableInsecureServer`, `insecurePort`, `enableSecureServer`. Errado: `enableHttp`, `httpPort`.
2. **HTTPS sobe por padrão.** Sem `enableSecureServer: false`, o plugin usa porta 27124 com cert inválido.
3. **Reiniciar Obsidian:** `taskkill /F /IM Obsidian.exe /T` (o `/T` mata processos filhos).

---

## PARTE 2 — Servidor MCP (escolha de pacote)

### Recomendado: `obsidian-mcp-server` (cyanheads) — leitura + escrita

Suporta: read, create, update, append, search, list, tags, frontmatter, mover, renomear.
**Requer:** plugin Local REST API rodando.

### Alternativa simples: `mcp-obsidian` (npm) — só leitura

Lê arquivos direto do disco, **não precisa do Local REST API**, mas só faz `read_notes` e `search_notes`.
Útil se você só quer consulta.

---

## PARTE 3 — Configuração por cliente MCP

> **Padrão importante (Windows):** sempre use o **caminho completo** para `npx.cmd`. Apps como Claude Desktop não herdam o PATH do sistema.
> Caminho típico: `C:\\Program Files\\nodejs\\npx.cmd` (note as barras duplas no JSON).
>
> **Linux/macOS:** basta `"command": "npx"`.

### Bloco padrão (válido para Claude Desktop, Claude Code, Cursor)

Nome do arquivo varia, mas o conteúdo é o mesmo:

```json
{
  "mcpServers": {
    "obsidian": {
      "command": "C:\\Program Files\\nodejs\\npx.cmd",
      "args": ["-y", "obsidian-mcp-server"],
      "env": {
        "OBSIDIAN_API_KEY": "SUA_API_KEY_AQUI",
        "OBSIDIAN_BASE_URL": "http://127.0.0.1:27123",
        "OBSIDIAN_VERIFY_SSL": "false",
        "MCP_TRANSPORT_TYPE": "stdio"
      }
    }
  }
}
```

### VS Code (formato diferente)

`Ctrl+Shift+P` → **MCP: Open User Configuration**:

```json
{
  "servers": {
    "obsidian": {
      "type": "stdio",
      "command": "C:\\Program Files\\nodejs\\npx.cmd",
      "args": ["-y", "obsidian-mcp-server"],
      "env": {
        "OBSIDIAN_API_KEY": "SUA_API_KEY_AQUI",
        "OBSIDIAN_BASE_URL": "http://127.0.0.1:27123",
        "OBSIDIAN_VERIFY_SSL": "false",
        "MCP_TRANSPORT_TYPE": "stdio"
      }
    }
  }
}
```

### Localizações dos arquivos por cliente

| Cliente | Caminho Windows | Caminho Linux/macOS |
|---------|-----------------|---------------------|
| Claude Desktop | `%APPDATA%\Claude\claude_desktop_config.json` | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Code | `%USERPROFILE%\.claude\claude_desktop_config.json` | `~/.claude/claude_desktop_config.json` |
| Cursor | `%USERPROFILE%\.cursor\mcp.json` | `~/.cursor/mcp.json` |
| VS Code | via comando `MCP: Open User Configuration` | idem |

---

## PARTE 4 — Variáveis de ambiente (referência)

| Variável | Obrigatório? | Default | Descrição |
|----------|--------------|---------|-----------|
| `OBSIDIAN_API_KEY` | Sim | — | API Key do plugin Local REST API |
| `OBSIDIAN_BASE_URL` | Recomendado | `https://127.0.0.1:27124` | URL completa (use HTTP se forçou HTTP) |
| `OBSIDIAN_VERIFY_SSL` | Recomendado | `true` | `false` para certificados auto-assinados ou HTTP |
| `MCP_TRANSPORT_TYPE` | Não | `stdio` | `stdio` para clientes locais |
| `OBSIDIAN_ENABLE_CACHE` | Não | `true` | Cache em memória |
| `OBSIDIAN_CACHE_REFRESH_INTERVAL_MIN` | Não | `10` | Refresh do cache (min) |

---

## PARTE 5 — Startup automático do Obsidian

Sem o Obsidian aberto, o plugin não responde e a IA não acessa o vault.

```powershell
$action = New-ScheduledTaskAction -Execute "C:\Program Files\Obsidian\Obsidian.exe"
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit 0 -StartWhenAvailable
Register-ScheduledTask -TaskName "Obsidian Startup" -Action $action -Trigger $trigger -Settings $settings -Force
```

**Linux (systemd user):**

```bash
mkdir -p ~/.config/systemd/user
cat > ~/.config/systemd/user/obsidian.service <<EOF
[Unit]
Description=Obsidian
After=graphical-session.target

[Service]
ExecStart=/usr/bin/obsidian
Restart=on-failure

[Install]
WantedBy=default.target
EOF
systemctl --user enable --now obsidian.service
```

---

## PARTE 6 — Validação final

Para cada cliente MCP configurado, executar **na ordem**:

1. **API respondendo:**
   ```bash
   curl -s http://127.0.0.1:27123/ -H "Authorization: Bearer $API_KEY"
   ```
   → Esperado: `"authenticated":true`

2. **MCP Server inicia sem erro:**
   ```bash
   OBSIDIAN_API_KEY=$API_KEY OBSIDIAN_BASE_URL=http://127.0.0.1:27123 OBSIDIAN_VERIFY_SSL=false npx -y obsidian-mcp-server
   ```
   → Esperado: nenhum erro, processo aguarda stdin

3. **Cliente carrega o servidor:**
   - Claude Desktop: `Settings → Developer` → `obsidian` ponto verde
   - Claude Code: `claude mcp list` mostra `obsidian`
   - VS Code: chat em modo Agent lista `obsidian` nas tools

4. **Comando real:**
   > "Liste os arquivos da pasta '01 - Cérebro' do meu vault Obsidian"
   → IA usa a tool MCP e retorna a lista

---

## PARTE 7 — Diagnóstico

### Logs

| Cliente | Local |
|---------|-------|
| Claude Desktop | `%APPDATA%\Claude\logs\mcp-server-obsidian.log` |
| Claude Code | `%USERPROFILE%\.claude\logs\` |
| VS Code | Output panel → "MCP" |

### Erros comuns

| Sintoma | Causa | Solução |
|---------|-------|---------|
| "Server transport closed unexpectedly" | `npx` não encontrado, ou args/env errados | Caminho completo de `npx.cmd` + checar log |
| "Unauthorized" / 401 | API key errada | Re-copiar do plugin |
| "ECONNREFUSED" | Obsidian fechado | Abrir Obsidian e aguardar 5s |
| `Usage: mcp-obsidian <vault-directory>` | Pacote errado (`mcp-obsidian` ≠ `obsidian-mcp-server`) | Trocar para `obsidian-mcp-server` |
| Plugin sobe em 27124 (HTTPS) e dá erro SSL | Falta `enableSecureServer: false` no data.json | Editar e reiniciar Obsidian |

---

## Estado atual desta instalação

| Componente | Status |
|------------|--------|
| Vault | `C:\Users\maycon\OneDrive\01_OBSIDIAN` |
| Node.js | v24.15.0 |
| Plugin Local REST API | v3.6.1 ativo, HTTP 27123 |
| API Key | configurada (ver `.obsidian/plugins/obsidian-local-rest-api/data.json`) |
| MCP Server | `obsidian-mcp-server` (cyanheads) — leitura + escrita |
| Claude Desktop | configurado |
| Claude Code | configurado |
| Cursor | configurado |
| VS Code | pendente (config não localizado) |
| Obsidian no startup | configurado (Task Scheduler) |

---

## Como uma IA agente usa este documento

Se você é uma IA com acesso a terminal, siga este fluxo de decisão:

1. Rode o curl da PARTE 6, item 1. **Falha?** → vá para PARTE 1.
2. Rode o teste do MCP Server, item 2. **Falha?** → vá para PARTE 2 e revise o pacote escolhido.
3. Verifique o config do cliente alvo na PARTE 3. **Faltando?** → use o bloco padrão.
4. Para Windows, **sempre** use `"command": "C:\\Program Files\\nodejs\\npx.cmd"`.
5. Em caso de erro, sempre leia primeiro o log em PARTE 7.

---

*Atualizado em: 2026-04-25*
