#!/usr/bin/env bash

set -e


BASEDIR=$(dirname "$0")
LOGFILE="$BASEDIR/hm-aquarium.log"

echo "Starting in background and writing log file to $LOGFILE"
nohup python3 -u "$BASEDIR/main.py" &>> "$LOGFILE" &
