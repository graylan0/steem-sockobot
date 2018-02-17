#!/bin/bash
until bot.py; do
    echo "'bot.py' crashed with exit code $?. Restarting..." >&2
    python3 ~/Python/steem-sockobot/bot.py
    sleep 1
done
