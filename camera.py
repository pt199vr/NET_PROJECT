import cv2
import time
"""
[ WARN:0@1.248] global ./modules/videoio/src/cap_gstreamer.cpp (2401) handleMessage OpenCV | GStreamer warning: Embedded video playback halted; module source reported: Could not read from resource.
[ WARN:0@1.249] global ./modules/videoio/src/cap_gstreamer.cpp (1356) open OpenCV | GStreamer warning: unable to start pipeline
[ WARN:0@1.249] global ./modules/videoio/src/cap_gstreamer.cpp (862) isPipelinePlaying OpenCV | GStreamer warning: GStreamer: pipeline have not been created
Snapshot taken and saved to /home/univr/Desktop/images/2024_05_26__23_46_00.jpg
Snapshot taken and saved to /home/univr/Desktop/images/2024_05_26__23_47_00.jpg
Snapshot taken and saved to /home/univr/Desktop/images/2024_05_26__23_48_00.jpg
"""
# Path to the camera device
#camera_device = '/dev/video0'

# Open a connection to the camera
#cap = cv2.VideoCapture(camera_device)

# GStreamer pipeline for the camera
gst_pipeline = "v4l2src device=/dev/video0 ! videoconvert ! appsink"

# Open the video capture with the GStreamer pipeline
cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

time_list = list([i for i in range(60) if i % 5 == 0])
print(time_list)      
# Set camera resolution
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Set MJPG format
#cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

# Check if the camera opened successfully
if not cap.isOpened():
   print(f"Error: Could not open camera device {camera_device}")
else:
   i = 0
   while i < 5:
      current_time = time.localtime()

      ret, frame = cap.read()
      # Display the frame
      #cv2.imshow('Camera', frame)

      # Check if seconds are 00
      if current_time.tm_sec in time_list:
         # Capture a single frame

         if ret:
            # Path to save the snapshot
            timestamp = time.strftime("%Y_%m_%d__%H_%M_%S")
            image_path = '/home/univr/Desktop/images/'+str(timestamp)+'.jpg'

            # Save the captured frame as an image file
            cv2.imwrite(image_path, frame)
            print(f"Snapshot taken and saved to {image_path}")
         else:
            print("Error: Could not read frame from camera")
         i=i+1
      time.sleep(1)

   # Release the camera
   cap.release()
   cv2.destroyAllWindows()
   print("Finish")
