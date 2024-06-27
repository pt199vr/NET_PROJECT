#!/usr/bin/python3
from picamera2 import Picamera2
import cv2
import time
import numpy as np
import os
from datetime import datetime
import csv
from PIL import Image

CAMERA_DEVICE_ID = 0
IMAGE_WIDTH = 640  # Increase resolution for better detection
IMAGE_HEIGHT = 480

#IMAGE_WIDTH = 320
#IMAGE_HEIGHT = 240
MOTION_BLUR = False
AREA_INSECT = [300,1000]

WRITE = True
SHOW = True
BACKGROUND = False

cnt_frame = 0
fps = 0
MSE_THRESHOLD = 50  # Lower threshold for detecting small movements
MSE_THRESHOLD = 1  # Lower threshold for detecting small movements


def mse(image_a, image_b):
    err = np.sum((image_a.astype("float") - image_b.astype("float")) ** 2)
    err /= float(image_a.shape[0] * image_a.shape[1])
    return err

def visualize_fps(image, fps: int):
    text_color = (0, 255, 0) if len(np.shape(image)) == 3 else (255, 255, 255)
    row_size = 20
    left_margin = 24

    font_size = 1
    font_thickness = 1

    fps_text = 'FPS = {:.1f}'.format(fps)
    text_location = (left_margin, row_size)
    cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                font_size, text_color, font_thickness)

    return image

if __name__ == "__main__":
    try:
        timestamp = datetime.now().strftime('%Y_%m_%d_%H-%M-%S')  # Format to milliseconds
            
        output_dir = 'images'
        csv_file = 'images/' + timestamp + '.csv'

        # Check if CSV file exists
        file_exists = os.path.isfile(csv_file)

        # Open CSV file in append mode
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Write the header only if the file didn't exist before
            if not file_exists:
                writer.writerow(['ImageName', 'Frame', 'Timestamp', 'x', 'y', 'w', 'h'])

            #cap = cv2.VideoCapture(CAMERA_DEVICE_ID)
            #cap.set(3, IMAGE_WIDTH)
            #cap.set(4, IMAGE_HEIGHT)
            picam2 = Picamera2()
            picam2.start()

            backSub = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=50, detectShadows=False)

            frame_gray_p = None

            while True:
                start_time = time.time()
                #ret, frame_raw = cap.read()
                pil_image = picam2.capture_image("main")
                
                frame_raw = np.array(pil_image)
                
                frame_raw = cv2.cvtColor(frame_raw, cv2.COLOR_RGB2BGR)  # Convert to BGR color space if necessary
                
                #if not ret:
                #    print("Failed to grab frame")
                #    break

                if MOTION_BLUR:
                    frame = cv2.GaussianBlur(frame_raw, (5, 5), 0)
                else:
                    frame = frame_raw
                
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                if BACKGROUND:
                    fg_mask = backSub.apply(frame)
                    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                else:
                    _, binary_image = cv2.threshold(frame_gray, 100, 255, cv2.THRESH_BINARY_INV)
                    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                #print(sum(sum(fg_mask)))
                #print(cv2.countNonZero(fg_mask))
                #hist = cv2.calcHist([fg_mask], [0], None, [256], [0,256])
                #print(hist.T)
                #print(sum(hist))
                #print("##################################")
                
                if len(contours) < 1500:
                    for i, contour in enumerate(contours):   
                         #print(i, cv2.contourArea(contour) )
                         #if AREA_INSECT[0] < cv2.contourArea(contour) < AREA_INSECT[1]:  # Adjust this value based on insect size
                         if cv2.contourArea(contour) > 10:       
                                (x, y, w, h) = cv2.boundingRect(contour)
                                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                cv2.putText(frame, "Insect Detected {} {}".format(i, cv2.contourArea(contour)), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                
                                #timestamp = time.strftime("%Y_%m_%d__%H_%M_%S_%f")
                                timestamp = datetime.now().strftime('%Y_%m_%d_%H-%M-%S.%f')[:-3]  # Format to milliseconds
            
                                cropped_image = frame_raw[y-10:y+h+10, x-10:x+w+10]
                                image_name = f'id_{i}_{timestamp}.jpg'
                                output_path = os.path.join(output_dir, f'id_{i}_{timestamp}.jpg')
                                
                                if WRITE:
                                    # Save the cropped image
                                    print(f'image to save: {image_name}')
                                    print(cropped_image)
                                    if not(cropped_image == []):
                                        cv2.imwrite(output_path, cropped_image)
                                        print(f'Saved cropped image: {image_name}')
                                        
                                        writer.writerow([image_name, cnt_frame, timestamp, x, y, w, h])
                    
                #frame_pil = cv2.cvtColor(frame_raw, cv2.COLOR_RGB2BGR)  # Convert to BGR color space if necessary
                frame_pil = Image.fromarray(frame_raw)
                
                print(fps)
                #cv2.imshow('Detection', visualize_fps(np.array(frame), fps))
                #cv2.imshow('Foreground Mask', visualize_fps(fg_mask, fps))

                if SHOW:
                    cv2.imshow('Frame', visualize_fps(np.array(frame_pil), fps))
                    cv2.imshow('Frame', visualize_fps(frame, fps))
                    
                    if BACKGROUND:
                        cv2.imshow('Foreground Mask', visualize_fps(fg_mask, fps))
                    else:
                        cv2.imshow('Foreground Mask', visualize_fps(binary_image, fps))
                #edges_50 = cv2.Canny(frame_gray, 50, 150)
                #edges = cv2.Canny(frame_gray, 10, 70)
                #cv2.imshow('Edges', visualize_fps(edges, fps))
                #cv2.imshow('Edges 50', visualize_fps(edges_50, fps))
                
                #if frame_gray_p is not None:
                #    if mse(frame_gray, frame_gray_p) > MSE_THRESHOLD:
                #        print('Frame {0}: Motion Detected!'.format(cnt_frame))
                
                end_time = time.time()
                seconds = end_time - start_time
                fps = 1.0 / seconds

                cnt_frame += 1
                frame_gray_p = frame_gray

                if cv2.waitKey(1) == 27:
                    break
    except Exception as e:
        print(e)
    finally:
        #cap.release()
        cv2.destroyAllWindows()
