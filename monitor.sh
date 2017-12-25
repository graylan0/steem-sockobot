#!/bin/bash
until bot.py; do
    echo "'bot.py' crashed with exit code $?. Restarting..." >&2
    TOKEN=$1 KEY=$2 NAME=jestemkioskiem python3 ~/steem-sockobot/bot.py
    sleep 1
done