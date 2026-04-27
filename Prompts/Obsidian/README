# Obsidian + MCP — Segundo Cérebro com IA

Conecte seu Obsidian a qualquer agente de IA usando o protocolo MCP.

Com essa configuração, o agente consegue ler, criar, editar e buscar notas no seu vault em tempo real. Você para de criar notas que ninguém usa e começa a ter um sistema que se mantém vivo sozinho.

Este documento funciona de duas formas: você segue o passo a passo manualmente, ou pede para uma IA agente com acesso a terminal executar por você.

---

## O que você vai conseguir fazer depois

- Pedir para o agente criar uma nota em qualquer pasta do vault
- Buscar conteúdo por texto, regex ou Dataview
- Atualizar status, tags e frontmatter de notas existentes
- Perguntar "onde eu falei sobre X?" e receber o caminho da nota
- Ter o agente registrar o resumo de cada sessão automaticamente

---

## Arquitetura

```
Vault Obsidian (.md no disco ou OneDrive)
        |
        v
Plugin "Local REST API"  -->  HTTP em 127.0.0.1:27123 (auth via API key)
        |
        v
Servidor MCP "obsidian-mcp-server" (cyanheads, via npx)
        |
        +--> Claude Desktop
        +--> Claude Code (CLI)
        +--> VS Code Copilot Agent
        +--> Cursor
        +--> Qualquer cliente MCP-compatível
```

---

## Pré-requisitos

| Item | Como verificar | Como instalar |
|------|----------------|---------------|
| Obsidian | Abrir o app | https://obsidian.md |
| Node.js 18+ | `node --version` | https://nodejs.org (LTS) |
| Cliente MCP | Claude Desktop / VS Code 1.99+ / Cursor | site oficial de cada um |

---

## Parte 1 — Plugin Local REST API

### Instalação automática (Windows)

Cole no PowerShell. Ajuste `$vault` para o caminho do seu vault antes de rodar.

```powershell
# Ajuste o caminho do seu vault aqui
$vault = "C:\Users\SEU_USUARIO\OneDrive\SEU_VAULT"
$pluginDir = "$vault\.obsidian\plugins\obsidian-local-rest-api"

# Gerar API key segura (64 hex)
$apiKey = -join ((1..32) | ForEach-Object { '{0:x2}' -f (Get-Random -Max 256) })

# Baixar plugin
New-Item -ItemType Directory -Force -Path $pluginDir | Out-Null
$base = "https://github.com/coddingtonbear/obsidian-local-rest-api/releases/latest/download"
Invoke-WebRequest "$base/manifest.json" -OutFile "$pluginDir\manifest.json" -UseBasicParsing
Invoke-WebRequest "$base/main.js"       -OutFile "$pluginDir\main.js"       -UseBasicParsing

# Configurar plugin (HTTP na porta 27123)
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
Write-Host "Guarde essa chave. Voce vai precisar dela na Parte 3."
Write-Host "Agora feche e reabra o Obsidian para ativar o plugin."
```

### Validar depois de reabrir o Obsidian

```bash
curl -s http://127.0.0.1:27123/ -H "Authorization: Bearer SUA_API_KEY"
```

Resposta esperada: `{"status":"OK","authenticated":true,...}`

### Erros comuns nessa etapa

**O plugin subiu na porta 27124 em vez de 27123**
Isso acontece porque o HTTPS sobe por padrão. Verifique se o `data.json` tem exatamente `"enableSecureServer": false`. Os nomes dos campos não seguem os da interface do plugin. Use os nomes exatos: `enableInsecureServer`, `insecurePort`, `enableSecureServer`.

**O Obsidian não recarregou o plugin**
Use `taskkill /F /IM Obsidian.exe /T` para garantir que os processos filhos também fecham. O `/T` é importante.

---

## Parte 2 — Servidor MCP

Duas opções de pacote. Escolha uma.

**Recomendado: `obsidian-mcp-server` (cyanheads)**
Suporta leitura, criação, edição, append, busca, tags, frontmatter, mover e renomear.
Requer o plugin Local REST API rodando.

**Alternativa simples: `mcp-obsidian`**
Lê arquivos direto do disco, sem precisar do plugin.
Só faz `read_notes` e `search_notes`. Útil se você só precisa de consulta.

---

## Parte 3 — Configurar o cliente MCP

O bloco de configuração é o mesmo para Claude Desktop, Claude Code e Cursor. Só o nome do arquivo muda.

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

> **Windows:** use sempre o caminho completo para `npx.cmd`. Aplicativos como o Claude Desktop não herdam o PATH do sistema. O caminho típico é `C:\\Program Files\\nodejs\\npx.cmd` com barras duplas dentro do JSON.
>
> **Linux e macOS:** troque `command` por `"npx"` apenas.

### Onde fica o arquivo de configuração

| Cliente | Windows | Linux e macOS |
|---------|---------|---------------|
| Claude Desktop | `%APPDATA%\Claude\claude_desktop_config.json` | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Code | `%USERPROFILE%\.claude\claude_desktop_config.json` | `~/.claude/claude_desktop_config.json` |
| Cursor | `%USERPROFILE%\.cursor\mcp.json` | `~/.cursor/mcp.json` |
| VS Code | `Ctrl+Shift+P` e buscar "MCP: Open User Configuration" | idem |

### VS Code usa um formato diferente

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

---

## Parte 4 — Variáveis de ambiente

| Variável | Obrigatório | Default | O que faz |
|----------|-------------|---------|-----------|
| `OBSIDIAN_API_KEY` | Sim | nenhum | API Key gerada na Parte 1 |
| `OBSIDIAN_BASE_URL` | Recomendado | `https://127.0.0.1:27124` | URL do plugin. Use HTTP se seguiu este guia |
| `OBSIDIAN_VERIFY_SSL` | Recomendado | `true` | Coloque `false` para HTTP ou certificado auto-assinado |
| `MCP_TRANSPORT_TYPE` | Não | `stdio` | Deixe como `stdio` para clientes locais |
| `OBSIDIAN_ENABLE_CACHE` | Não | `true` | Cache em memória |
| `OBSIDIAN_CACHE_REFRESH_INTERVAL_MIN` | Não | `10` | Intervalo de atualização do cache em minutos |

---

## Parte 5 — Subir o Obsidian automaticamente no login

O plugin só responde enquanto o Obsidian estiver aberto. Para não precisar lembrar de abrir:

**Windows (Task Scheduler)**

```powershell
$action   = New-ScheduledTaskAction -Execute "C:\Program Files\Obsidian\Obsidian.exe"
$trigger  = New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME
$settings = New-ScheduledTaskSettingsSet -ExecutionTimeLimit 0 -StartWhenAvailable
Register-ScheduledTask -TaskName "Obsidian Startup" -Action $action -Trigger $trigger -Settings $settings -Force
```

**Linux (systemd user)**

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

## Parte 6 — Validação final

Rode na ordem. Se um passo falhar, resolva antes de avançar.

**1. API respondendo**

```bash
curl -s http://127.0.0.1:27123/ -H "Authorization: Bearer SUA_API_KEY"
```

Esperado: `"authenticated":true`

**2. MCP Server sobe sem erro**

```bash
OBSIDIAN_API_KEY=SUA_API_KEY \
OBSIDIAN_BASE_URL=http://127.0.0.1:27123 \
OBSIDIAN_VERIFY_SSL=false \
npx -y obsidian-mcp-server
```

Esperado: processo aguarda stdin sem mostrar erro.

**3. Cliente reconhece o servidor**

- Claude Desktop: Settings > Developer > ponto verde ao lado de "obsidian"
- Claude Code: `claude mcp list` mostra "obsidian"
- VS Code: modo Agent lista "obsidian" nas tools disponíveis

**4. Teste real**

Pergunte ao agente:

> "Liste os arquivos da raiz do meu vault Obsidian"

Se ele responder com a lista de pastas e arquivos, está funcionando.

---

## Parte 7 — Diagnóstico

### Onde ficam os logs

| Cliente | Caminho |
|---------|---------|
| Claude Desktop | `%APPDATA%\Claude\logs\mcp-server-obsidian.log` |
| Claude Code | `%USERPROFILE%\.claude\logs\` |
| VS Code | painel Output, selecionar "MCP" |

### Erros mais comuns

| O que aparece | Por que acontece | Como resolver |
|---------------|-----------------|---------------|
| "Server transport closed unexpectedly" | `npx` não encontrado ou variáveis de ambiente erradas | Use o caminho completo de `npx.cmd` e verifique o log |
| "Unauthorized" ou 401 | API key errada ou copiada com espaço | Re-copie a chave direto do `data.json` do plugin |
| "ECONNREFUSED" | Obsidian está fechado | Abra o Obsidian e aguarde 5 segundos |
| `Usage: mcp-obsidian <vault-directory>` | Pacote errado instalado | Troque para `obsidian-mcp-server`, são pacotes diferentes |
| Plugin subiu na porta 27124 com erro SSL | Falta `"enableSecureServer": false` no `data.json` | Edite o arquivo e reinicie o Obsidian |

---

## Para IAs agente com acesso a terminal

Se você é uma IA executando este documento, siga este fluxo:

1. Rode o curl da Parte 6, item 1. Falhou? Vá para a Parte 1.
2. Teste o MCP Server, item 2 da Parte 6. Falhou? Revise o pacote na Parte 2.
3. Verifique o arquivo de config do cliente alvo na Parte 3. Falta o bloco? Adicione o bloco padrão.
4. No Windows, sempre use `"command": "C:\\Program Files\\nodejs\\npx.cmd"`.
5. Qualquer erro: leia o log primeiro (Parte 7) antes de tentar outra solução.
