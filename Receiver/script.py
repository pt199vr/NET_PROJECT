import subprocess
import os

folder_path = "images/"

#subprocess.run(['python', 'lora_rx.py'])

folder_contents = os.listdir(folder_path)
while len(folder_contents)>0:
	subprocess.run(['python', 'client.py'])
