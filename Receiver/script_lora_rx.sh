#!/bin/bash
source ~/Desktop/NET_PROJECT/Receiver/.env/bin/activate
nohup /usr/bin/python3 ~/Desktop/NET_PROJECT/Receiver/script.py > ~/Desktop/NET_PROJECT/insect.log 2>&1 &
