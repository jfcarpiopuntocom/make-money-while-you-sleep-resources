#!/bin/bash
# 4-Pick-an-Old-Session.command (Mac): choose an earlier conversation from a list (claude --resume).
exec "$(dirname "$0")/2-Start-My-Studio.command" --resume
