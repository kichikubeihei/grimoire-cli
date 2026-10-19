#!/usr/bin/env bash
# Grimoire Algorithmica: Summon Arcane Familiar (Mac / Linux Installer)
set -e

FAMILIAR_DIR="$HOME/.grimoire"
mkdir -p "$FAMILIAR_DIR"

echo -e "\033[96m"
cat << "EOF"
  ██████╗ ██████╗ ██╗███╗   ███╗ ██████╗ ██╗██████╗ ███████╗
 ██╔════╝ ██╔══██╗██║████╗ ████║██╔═══██╗██║██╔══██╗██╔════╝
 ██║  ███╗██████╔╝██║██╔████╔██║██║   ██║██║██████╔╝█████╗  
 ██║   ██║██╔══██╗██║██║╚██╔╝██║██║   ██║██║██╔══██╗██╔══╝  
 ╚██████╔╝██║  ██║██║██║ ╚═╝ ██║╚██████╔╝██║██║  ██║███████╗
  ╚═════╝ ╚═╝  ╚═╝╚═╝╚═╝     ╚═╝ ╚═════╝ ╚═╝╚═╝  ╚═╝╚══════╝
           --- THE ARCANE FAMILIAR DAEMON ---
EOF
echo -e "\033[0m"

echo "[*] Inscribing Arcane Familiar into $FAMILIAR_DIR..."
curl -fsSL "https://raw.githubusercontent.com/kichikubeihei/grimoire-cli/main/grimoire-familiar.py" -o "$FAMILIAR_DIR/familiar.py"
chmod +x "$FAMILIAR_DIR/familiar.py"

if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "[!] Error: Python 3.8+ is required to awaken the Familiar."
    exit 1
fi

echo "[*] Awakening Familiar with $PYTHON_CMD..."
if [ -n "$GRIMOIRE_API_KEY" ]; then
    exec "$PYTHON_CMD" "$FAMILIAR_DIR/familiar.py" --api-key "$GRIMOIRE_API_KEY" "$@"
else
    exec "$PYTHON_CMD" "$FAMILIAR_DIR/familiar.py" "$@"
fi
