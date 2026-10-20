#!/bin/bash
# 2-Start-My-Studio.command (Mac)
# Double-click me every time you want to work. I open your My-Studio folder
# and start Claude Code inside it. 3- and 4- call me with --continue or --resume.
HERE="$(cd "$(dirname "$0")" && pwd)"
STUDIO="$HERE/My-Studio"
[ -f "$STUDIO/CLAUDE.md" ] || STUDIO="$HOME/My-Studio"
if [ ! -f "$STUDIO/CLAUDE.md" ]; then
  echo " I cannot find your My-Studio folder. Put it next to this file, or in your home folder."
  read -r -p " Press Enter to close... "; exit 1
fi
# The official installer puts claude in ~/.local/bin.
CLAUDE="$(command -v claude || echo "$HOME/.local/bin/claude")"
if [ ! -x "$CLAUDE" ]; then
  echo " Claude Code is not installed yet. Double-click 1-Install-Claude.command first."
  read -r -p " Press Enter to close... "; exit 1
fi
# Let Claude read the Master Prompts in the kit's prompts folder (if it is there).
EXTRA=()
[ -d "$HERE/../prompts" ] && EXTRA=(--add-dir "$(cd "$HERE/../prompts" && pwd)")
cd "$STUDIO" || exit 1
echo " Opening your studio. Type to Claude in plain words. Esc stops it. /exit leaves."
"$CLAUDE" "${EXTRA[@]}" "$@"
