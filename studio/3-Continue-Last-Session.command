#!/bin/bash
# 3-Continue-Last-Session.command (Mac): pick up where you left off (claude --continue).
exec "$(dirname "$0")/2-Start-My-Studio.command" --continue
