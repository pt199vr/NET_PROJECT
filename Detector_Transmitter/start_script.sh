#!/bin/bash
nohup /usr/bin/python3 ~/Desktop/NET_PROJECT/Detector_Transmitter/pi_insect.py > ~/Desktop/NET_PROJECT/pi_insect.log 2>&1 &
echo $! > ~/Desktop/NET_PROJECT/script.pid
