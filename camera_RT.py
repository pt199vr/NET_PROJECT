import cv2

# Open the default camera (index 0)
#cap = cv2.VideoCapture(0)

# GStreamer pipeline for the camera
gst_pipeline = "v4l2src device=/dev/video0 ! videoconvert ! appsink"

# Open the video capture with the GStreamer pipeline
cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

# Check if the camera opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# Main loop to capture and display frames
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if the frame was captured successfully
    if not ret:
        print("Error: Could not read frame.")
        break

    # Display the frame
    cv2.imshow('Camera', frame)

    # Check for key press
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # Press 'q' to exit
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
