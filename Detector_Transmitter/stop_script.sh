#!/bin/bash
if [ -f ~/Desktop/NET_PROJECT/script.pid ]; then
    PID=$(cat ~/Desktop/NET_PROJECT/script.pid)
    kill $PID
    rm ~/Desktop/NET_PROJECT/script.pid
fi
