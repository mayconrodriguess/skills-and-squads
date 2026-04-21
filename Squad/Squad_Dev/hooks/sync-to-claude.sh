#!/bin/bash
# Squad Dev — Sincroniza escolhas de hooks para .claude/settings.json
# Chamado automaticamente pelo setup.sh após configurar o husky.
# Garante que Claude Code e qualquer IA usem as mesmas regras.

CHOICES="${1:-7}"
SETTINGS=".claude/settings.json"
mkdir -p .claude

echo "  Gerando $SETTINGS..."

# Base sempre presente (proteção e log)
cat > "$SETTINGS" << 'BASE'
{
  "hooks": {
    "PostToolUse": [],
    "PreToolUse": [
      {
        "_comment": "Bloquear arquivos protegidos — espelho do pre-commit universal",
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"\nimport os,sys,json\np=os.environ.get('CLAUDE_TOOL_INPUT_FILE_PATH','')\nblocked=['.env','.env.production','.env.prod','id_rsa','id_ed25519']\nbad_dirs=['node_modules','.git']\nname=os.path.basename(p)\nif name in blocked or any(d in p for d in bad_dirs):\n    print(json.dumps({'decision':'block','reason':f'Arquivo protegido: {p}'}))\n    sys.exit(0)\nprint(json.dumps({'decision':'approve'}))\n\""
          }
        ]
      },
      {
        "_comment": "Bloquear comandos destrutivos — espelho do pre-push universal",
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 -c \"\nimport os,sys,json\ncmd=os.environ.get('CLAUDE_TOOL_INPUT_COMMAND','')\ndangerous=['rm -rf /','git push --force origin main','git push --force origin master','DROP DATABASE','truncate production']\nfor d in dangerous:\n    if d.lower() in cmd.lower():\n        print(json.dumps({'decision':'block','reason':f'Comando perigoso bloqueado: {d}'}))\n        sys.exit(0)\nprint(json.dumps({'decision':'approve'}))\n\""
          }
        ]
      }
    ],
    "Stop": [],
    "Notification": [
      {
        "_comment": "Log de notificações — espelho do commit-log universal",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"[$(date -u +%Y-%m-%dT%H:%M:%SZ)] NOTIFY: $CLAUDE_NOTIFICATION_MESSAGE\" >> production_artifacts/memory/command-log.txt 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
BASE

# Adicionar hooks conforme escolhas
add_prettier() {
  python3 - << 'PY'
import json
with open('.claude/settings.json') as f: s = json.load(f)
s['hooks']['PostToolUse'].append({
  "_comment": "Prettier — espelho do lint-staged universal",
  "matcher": "Edit|Write",
  "hooks": [{"type": "command", "command": "npx prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\" 2>/dev/null || true"}]
})
with open('.claude/settings.json', 'w') as f: json.dump(s, f, indent=2)
PY
}

add_eslint() {
  python3 - << 'PY'
import json
with open('.claude/settings.json') as f: s = json.load(f)
s['hooks']['PostToolUse'].append({
  "_comment": "ESLint --fix — espelho do lint-staged universal",
  "matcher": "Edit|Write",
  "hooks": [{"type": "command", "command": "case \"$CLAUDE_TOOL_INPUT_FILE_PATH\" in *.js|*.jsx|*.ts|*.tsx) npx eslint --fix \"$CLAUDE_TOOL_INPUT_FILE_PATH\" 2>/dev/null || true ;; esac"}]
})
with open('.claude/settings.json', 'w') as f: json.dump(s, f, indent=2)
PY
}

add_commit_log() {
  python3 - << 'PY'
import json
with open('.claude/settings.json') as f: s = json.load(f)
s['hooks']['PostToolUse'].append({
  "_comment": "Log de comandos Bash — compliance",
  "matcher": "Bash",
  "hooks": [{"type": "command", "command": "echo \"[$(date -u +%Y-%m-%dT%H:%M:%SZ)] CMD: $CLAUDE_TOOL_INPUT_COMMAND\" >> production_artifacts/memory/command-log.txt 2>/dev/null || true"}]
})
with open('.claude/settings.json', 'w') as f: json.dump(s, f, indent=2)
PY
}

add_notify() {
  python3 - << 'PY'
import json
with open('.claude/settings.json') as f: s = json.load(f)
s['hooks']['Stop'].append({
  "_comment": "Notificação desktop quando Claude termina — espelho do post-commit universal",
  "hooks": [{"type": "command", "command": "if command -v osascript &>/dev/null; then osascript -e 'display notification \"Squad Dev terminou.\" with title \"Claude Code\"' 2>/dev/null; elif command -v notify-send &>/dev/null; then notify-send 'Claude Code' 'Squad Dev terminou.' 2>/dev/null; fi; true"}]
})
with open('.claude/settings.json', 'w') as f: json.dump(s, f, indent=2)
PY
}

case "$CHOICES" in
  *7*|*"todos"*)
    add_prettier; add_eslint; add_notify; add_commit_log ;;
  *)
    echo "$CHOICES" | grep -q "1" && add_prettier
    echo "$CHOICES" | grep -q "2" && add_eslint
    echo "$CHOICES" | grep -q "5" && add_commit_log
    echo "$CHOICES" | grep -q "6" && add_notify
    ;;
esac

echo "  OK — .claude/settings.json sincronizado com as escolhas do husky."
