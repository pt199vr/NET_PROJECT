# NET_PROJECT


#Create a virtual environment
python3 -m venv --system-site-packages new_env

#Activate the new environment
source new_env/bin/activate

#Update pip
pip install --upgrade pip

#Install mediapipe
pip install mediapipe

#Install OpenCV
pip install opencv-python

#Check if you have all the libraries available
pip list

You must see "picamera2" in the list when using "pip list"
