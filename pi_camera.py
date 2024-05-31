from picamera2 import Picamera2
import time

def capture_image(output_file):
    # Initialize the camera
    picam2 = Picamera2()

    # Configure the camera
    camera_config = picam2.create_still_configuration()
    picam2.configure(camera_config)

    # Start the camera
    picam2.start()

    # Allow the camera to warm up
    time.sleep(2)

    # Capture the image
    picam2.capture_file(output_file)

    # Stop the camera
    picam2.stop()

    print(f"Image saved as {output_file}")

if __name__ == "__main__":
    output_file = "captured_image.jpg"
    capture_image(output_file)
