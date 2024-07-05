#!/bin/bash
source ~/Desktop/NET_PROJECT/Detector_Transmitter/.env/bin/activate
nohup /usr/bin/python3 ~/Desktop/NET_PROJECT/Detector_Transmitter/insect.py > ~/Desktop/NET_PROJECT/insect.log 2>&1 &
echo $! > ~/Desktop/NET_PROJECT/script.pid
