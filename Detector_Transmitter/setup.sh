#!/bin/bash

# Create a virtual environment
python3 -m venv --system-site-packages .env

# Activate the new environment
source .env/bin/activate

# Update pip
pip install --upgrade pip

# Install mediapipe
pip install mediapipe

# Install OpenCV
pip install opencv-python

pip install Pillow

pip install --upgrade pyLoraRFM9x
