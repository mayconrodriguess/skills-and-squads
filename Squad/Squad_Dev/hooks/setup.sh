#!/bin/bash
# Squad Dev — Universal Hooks Setup (husky)
# Funciona em qualquer IA. Roda via git hooks, não depende do Claude.
# Executar a partir da raiz do projeto: bash Squad_Dev/hooks/setup.sh

set -e

APP_DIR="app_build"
HOOKS_DIR="$APP_DIR/.husky"

echo ""
echo "Squad Dev — Configuração de Hooks Universais"
echo "============================================="
echo "Estes hooks rodam via git — funcionam com Claude, Cursor, Copilot ou qualquer IA."
echo ""

# Verificar se app_build existe
if [ ! -d "$APP_DIR" ]; then
  echo "Criando $APP_DIR..."
  mkdir -p "$APP_DIR"
fi

# Verificar se há package.json em app_build
if [ ! -f "$APP_DIR/package.json" ]; then
  echo "Nenhum package.json em $APP_DIR. Inicializando..."
  cd "$APP_DIR" && npm init -y && cd ..
fi

echo ""
echo "Quais hooks deseja ativar?"
echo ""
echo "  [1] Formatação automática (Prettier)        — recomendado"
echo "  [2] Lint automático (ESLint --fix)           — recomendado"
echo "  [3] Proteção de arquivos sensíveis (.env)   — recomendado"
echo "  [4] Bloquear push com testes falhando       — recomendado"
echo "  [5] Log de commits (compliance)             — opcional"
echo "  [6] Notificação no terminal ao commitar     — opcional"
echo "  [7] Todos os recomendados (1,2,3,4)"
echo "  [0] Nenhum — configurar manualmente depois"
echo ""
read -p "Escolha (ex: 1,3,4 ou 7): " CHOICES

echo ""
echo "Instalando husky e lint-staged em $APP_DIR..."
cd "$APP_DIR"
npm install --save-dev husky lint-staged 2>/dev/null

npx husky init 2>/dev/null || true

# Garantir que husky está no prepare script
node -e "
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
if (!pkg.scripts) pkg.scripts = {};
pkg.scripts.prepare = 'husky';
fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
"
cd ..

# Função: instalar Prettier
install_prettier() {
  echo "  Configurando Prettier..."
  cd "$APP_DIR"
  npm install --save-dev prettier 2>/dev/null

  cat > .prettierrc.json << 'EOF'
{
  "semi": true,
  "singleQuote": true,
  "trailingComma": "es5",
  "printWidth": 100,
  "tabWidth": 2
}
EOF

  # Adicionar ao lint-staged
  node -e "
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
if (!pkg['lint-staged']) pkg['lint-staged'] = {};
pkg['lint-staged']['*.{js,jsx,ts,tsx,css,md,json}'] = pkg['lint-staged']['*.{js,jsx,ts,tsx,css,md,json}'] || [];
if (!pkg['lint-staged']['*.{js,jsx,ts,tsx,css,md,json}'].includes('prettier --write'))
  pkg['lint-staged']['*.{js,jsx,ts,tsx,css,md,json}'].push('prettier --write');
fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
"
  cd ..
  echo "  OK — Prettier configurado."
}

# Função: instalar ESLint
install_eslint() {
  echo "  Configurando ESLint..."
  cd "$APP_DIR"
  npm install --save-dev eslint 2>/dev/null

  node -e "
const fs = require('fs');
const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
if (!pkg['lint-staged']) pkg['lint-staged'] = {};
const key = '*.{js,jsx,ts,tsx}';
pkg['lint-staged'][key] = pkg['lint-staged'][key] || [];
if (!pkg['lint-staged'][key].includes('eslint --fix'))
  pkg['lint-staged'][key].push('eslint --fix');
fs.writeFileSync('package.json', JSON.stringify(pkg, null, 2));
"
  cd ..
  echo "  OK — ESLint configurado."
}

# Função: proteção de arquivos sensíveis
install_secret_guard() {
  echo "  Configurando proteção de arquivos sensíveis..."
  mkdir -p "$HOOKS_DIR"
  cat > "$HOOKS_DIR/pre-commit" << 'HOOK'
#!/bin/sh
# Squad Dev — Secret Guard (universal, funciona em qualquer IA)

BLOCKED=$(git diff --cached --name-only | grep -E '\.env$|\.env\.production|\.env\.prod|id_rsa|id_ed25519|\.pem$|\.key$|credentials\.json|secrets\.' || true)

if [ -n "$BLOCKED" ]; then
  echo ""
  echo "BLOQUEADO: Arquivo protegido detectado no commit:"
  echo "$BLOCKED"
  echo ""
  echo "Remova com: git restore --staged <arquivo>"
  echo ""
  exit 1
fi

# Checar conteúdo por padrões de secret
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.(js|ts|tsx|jsx|py|go|rb|sh|yml|yaml|json|env)$' || true)
if [ -n "$STAGED_FILES" ]; then
  SECRETS=$(git diff --cached | grep -E '(AKIA|sk_live_|pk_live_|ghp_|gho_|github_pat_|xoxb-|xoxp-)' || true)
  if [ -n "$SECRETS" ]; then
    echo ""
    echo "BLOQUEADO: Possível secret detectado no diff."
    echo "Revise antes de commitar."
    echo ""
    exit 1
  fi
fi

# Rodar lint-staged se existir
if [ -f "package.json" ] && grep -q "lint-staged" package.json 2>/dev/null; then
  npx lint-staged 2>/dev/null || exit 1
fi

exit 0
HOOK
  chmod +x "$HOOKS_DIR/pre-commit"
  cd ..
  echo "  OK — Secret guard configurado."
}

# Função: bloquear push com testes falhando
install_test_guard() {
  echo "  Configurando test guard no pre-push..."
  mkdir -p "$HOOKS_DIR"
  cat > "$HOOKS_DIR/pre-push" << 'HOOK'
#!/bin/sh
# Squad Dev — Test Guard (universal)
cd app_build 2>/dev/null || true

if [ -f "package.json" ]; then
  if grep -q '"test"' package.json; then
    echo "Rodando testes antes do push..."
    npm test --if-present 2>&1
    if [ $? -ne 0 ]; then
      echo ""
      echo "BLOQUEADO: Testes falharam. Push cancelado."
      echo "Corrija os erros antes de publicar."
      echo ""
      exit 1
    fi
  fi
fi

exit 0
HOOK
  chmod +x "$HOOKS_DIR/pre-push"
  cd ..
  echo "  OK — Test guard configurado."
}

# Função: log de commits
install_commit_log() {
  echo "  Configurando log de commits..."
  mkdir -p "$HOOKS_DIR"
  cat > "$HOOKS_DIR/post-commit" << 'HOOK'
#!/bin/sh
# Squad Dev — Commit Log (compliance)
LOG_FILE="production_artifacts/memory/command-log.txt"
mkdir -p production_artifacts/memory 2>/dev/null
HASH=$(git rev-parse --short HEAD)
MSG=$(git log -1 --pretty=%s)
BRANCH=$(git branch --show-current)
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] COMMIT: $HASH | $BRANCH | $MSG" >> "../$LOG_FILE" 2>/dev/null || true
exit 0
HOOK
  chmod +x "$HOOKS_DIR/post-commit"
  cd ..
  echo "  OK — Commit log configurado."
}

# Função: notificação no terminal
install_notify() {
  echo "  Configurando notificação..."
  mkdir -p "$HOOKS_DIR"
  cat >> "$HOOKS_DIR/post-commit" << 'HOOK'

# Notificação
if command -v osascript >/dev/null 2>&1; then
  osascript -e 'display notification "Commit realizado com sucesso." with title "Squad Dev"' 2>/dev/null || true
elif command -v notify-send >/dev/null 2>&1; then
  notify-send "Squad Dev" "Commit realizado com sucesso." 2>/dev/null || true
fi
HOOK
  cd ..
  echo "  OK — Notificação configurada."
}

# Processar escolhas
case "$CHOICES" in
  *7*|*"todos"*)
    install_prettier
    install_eslint
    install_secret_guard
    install_test_guard
    ;;
  *0*)
    echo "Nenhum hook configurado. Edite $HOOKS_DIR/ manualmente quando quiser."
    ;;
  *)
    echo "$CHOICES" | grep -q "1" && install_prettier
    echo "$CHOICES" | grep -q "2" && install_eslint
    echo "$CHOICES" | grep -q "3" && install_secret_guard
    echo "$CHOICES" | grep -q "4" && install_test_guard
    echo "$CHOICES" | grep -q "5" && install_commit_log
    echo "$CHOICES" | grep -q "6" && install_notify
    ;;
esac

# Sincronizar com .claude/settings.json
echo ""
echo "Sincronizando com .claude/settings.json (camada Claude Code)..."
bash "$(dirname "$0")/sync-to-claude.sh" "$CHOICES" 2>/dev/null || echo "  (sync-to-claude.sh não encontrado — ignorar se não usar Claude Code)"

echo ""
echo "Hooks configurados com sucesso."
echo "Funcionam via git em qualquer IA (Claude, Cursor, Copilot, Windsurf, etc.)"
echo ""
echo "Para ver ou editar: ls $HOOKS_DIR/"
echo "Para o Claude Code: .claude/settings.json"
echo ""
