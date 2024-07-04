<<<<<<< HEAD
#INTRODUCTION
The projec aims to create a system that recognizes insects in the crop fields.
The system is composed by 3 main devices:
    1) Raspberry 3B used for the insect capturing through a camera and delivers all the insects images to the raspberry 2,
    2) Raspberry 2 which gets pictures from all the raspeberries 3B distributed in the field and sends them to you local pc for classification and for calculating statistics through internet,
    3) A pc that gets all the pictures and do the calculation on them.

#REQUIREMENTS
In order to correctly use the code you need to install those libraries on each devide:

    PC requirements:
        pip update
        pip upgrade
        pip install csv
        pip install opencv-python  
        pip install numpy
        pip install Pillow
=======
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
>>>>>>> bae66fbe7ea3c6c2155454363710156aacb809be
