#!/bin/bash
if [ -f /home/univr/Desktop/images/your_script.pid ]; then
    PID=$(cat /home/univr/Desktop/images/your_script.pid)
    kill $PID
    rm /home/univr/Desktop/images/your_script.pid
fi
