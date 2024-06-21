from picamera2 import Picamera2
import time

from datetime import datetime
import os

def capture_image(output_file):
    # Initialize the camera
    picam2 = Picamera2()

    # Configure the camera
    camera_config = picam2.create_still_configuration()
    picam2.configure(camera_config)

    # Start the camera
    picam2.start()

    # Allow the camera to warm up
    time.sleep()

    # Capture the image
    picam2.capture_file(output_file)

    # Stop the camera
    picam2.stop()

    print(f"Image saved as {output_file}")

def once():
	    # Initialize the camera
    picam2 = Picamera2()

    # Configure the camera
    camera_config = picam2.create_still_configuration()
    picam2.configure(camera_config)

    # Start the camera
    picam2.start()
	
    output_dir = '/home/univr/Desktop/images'
    
    while True:
      timestamp = datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')[:-3]  # Format to milliseconds
              
      output_file = os.path.join(output_dir, f'{timestamp}.jpg')
      # Allow the camera to warm up
      time.sleep(30)

      # Capture the image
      picam2.capture_file(output_file)

	  #print(f"Image saved as {output_file}")

    # Stop the camera
    picam2.stop()
    
if __name__ == "__main__":
	once()
    #output_file = "captured_image.jpg"
    #capture_image(output_file)
