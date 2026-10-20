#!/bin/bash
# 1-Install-Claude.command (Mac)
# Double-click me once. I run the official Claude Code installer from Anthropic
# (the same command shown at https://code.claude.com/docs/en/setup). No admin password needed.
echo
echo " Hello! I am going to install Claude Code, your AI assistant."
echo " It can take a few minutes and may show no progress. That is normal."
echo
read -r -p " Press Enter to start... "
curl -fsSL https://claude.ai/install.sh | bash
echo
echo " Done. Next step: close this window and double-click 2-Start-My-Studio.command"
echo " If you saw an error, copy it and paste it into claude.ai in your browser."
read -r -p " Press Enter to close... "
