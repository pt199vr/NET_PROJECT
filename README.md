#INTRODUCTION
The project aims to create a system that recognizes insects in the crop fields.
The system is composed by 3 main devices:
    1) Raspberry 3B used for the insect capturing through a camera and delivers all the insects images to the raspberry 2,
    2) Raspberry 2 which gets pictures from all the raspeberries 3B distributed in the field and sends them to you local pc for classification and for calculating statistics through internet,
    3) A pc that gets all the pictures and do the calculation on them.

First of all, clone this repository:
```bash
git clone https://github.com/pt199vr/NET_PROJECT
```
#REQUIREMENTS
In order to correctly use the code you need to install those libraries and set up the environment for each device:

    PC requirements:
        pip update
        pip upgrade
        pip install csv
        pip install opencv-python  
        pip install numpy
        pip install Pillow

    Raspberry 2:
        cd NET_PROJECT/Receiver
        ./setup.sh
    Raspberry 3B:
        cd NET_PROJECT/Detector_Transmitter
        ./setup.sh

#CLONE THE REPOSITORY
git clone link_to_the_repository

#EXECUTION COMMAND

    PC:
        cd PC_CODE/
        #The following command is a python code that classifies and compute statistics automatically
        python pc_code.py
        #use the following commands to the task in steps

    Raspberry 2:
        cd NET_PROJECT/Receiver
        source .env/bin/activate
        python script.py
        
    Raspberry 3B:
        cd NET_PROJECT/Detector_Transmitter
        source .env/bin/activate
        ./start_script.sh
        ./stop_script.sh

#WARNING!
Check always that the IP address sets in the PC_CODE/server.py(line 20) and in the Receiver/client.py (line30) are compatible.
You may overwrite the IP address if the pc has a different IP respect to the previous day .
