#!/bin/bash
nohup /usr/bin/python3 /home/univr/Desktop/NET_PROJECT/pi_camera.py > /home/univr/Desktop/images/your_script.log 2>&1 &
echo $! > /home/univr/Desktop/images/your_script.pid
