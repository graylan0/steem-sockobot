#!/bin/bash
# MIND THAT IF YOU RUN THIS IN CRONTAB, YOU NEED TO CHECK YOUR SYSTEM VARS - THEY MAY DIFFER. WHICH IS WHY I PROVIDED VARIABLES HERE.
until bot.py; do
    echo "'bot.py' crashed with exit code $?. Restarting..." >&2
    SB_TOKEN=$1 SB_KEY=$2 SB_NAME=$3 python3 ~/Python/steem-sockobot/bot.py
    sleep 1
done
