#!/usr/bin/python3

import cv2
import time
import numpy as np
import os
from datetime import datetime
import csv

CAMERA_DEVICE_ID = 0
IMAGE_WIDTH = 640  # Increase resolution for better detection
IMAGE_HEIGHT = 480

#IMAGE_WIDTH = 320
#IMAGE_HEIGHT = 240
MOTION_BLUR = True
AREA_INSECT = [300,1000]

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
        output_dir = '/home/univr/Desktop/images'
        csv_file = '/home/univr/Desktop/cropped_images_info.csv'

        # Check if CSV file exists
        file_exists = os.path.isfile(csv_file)

        # Open CSV file in append mode
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            
            # Write the header only if the file didn't exist before
            if not file_exists:
                writer.writerow(['ImageName', 'Timestamp', 'x', 'y', 'w', 'h'])

            cap = cv2.VideoCapture(CAMERA_DEVICE_ID)
            cap.set(3, IMAGE_WIDTH)
            cap.set(4, IMAGE_HEIGHT)

            backSub = cv2.createBackgroundSubtractorMOG2(history=50, varThreshold=50, detectShadows=False)

            frame_gray_p = None

            while True:
                start_time = time.time()
                ret, frame_raw = cap.read()

                if not ret:
                    print("Failed to grab frame")
                    break

                if MOTION_BLUR:
                    frame = cv2.GaussianBlur(frame_raw, (5, 5), 0)
                else:
                    frame = frame_raw

                fg_mask = backSub.apply(frame)
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
                print(sum(sum(fg_mask)))
                print(cv2.countNonZero(fg_mask))
                #hist = cv2.calcHist([fg_mask], [0], None, [256], [0,256])
                #print(hist.T)
                #print(sum(hist))
                print("##################################")
                
                contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                if len(contours) < 15:
                    for i, contour in enumerate(contours):   
                         print(i, cv2.contourArea(contour) )
                         if AREA_INSECT[0] < cv2.contourArea(contour) < AREA_INSECT[1]:  # Adjust this value based on insect size
                                
                                (x, y, w, h) = cv2.boundingRect(contour)
                                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                                cv2.putText(frame, "Insect Detected {} {}".format(i, cv2.contourArea(contour)), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                                
                                #timestamp = time.strftime("%Y_%m_%d__%H_%M_%S_%f")
                                timestamp = datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')[:-3]  # Format to milliseconds
            
                                cropped_image = frame_raw[y-10:y+h+10, x-10:x+w+10]
                                image_name = f'id_{i}_{timestamp}.jpg'
                                output_path = os.path.join(output_dir, f'id_{i}_{timestamp}.jpg')
                
                                # Save the cropped image
                                cv2.imwrite(output_path, cropped_image)
                                print(f'Saved cropped image: {image_name}')
                                
                                writer.writerow([image_name, timestamp, x, y, w, h])
                                
                cv2.imshow('Frame', visualize_fps(frame, fps))
                cv2.imshow('Foreground Mask', visualize_fps(fg_mask, fps))

                #edges_50 = cv2.Canny(frame_gray, 50, 150)
                #edges = cv2.Canny(frame_gray, 10, 70)
                #cv2.imshow('Edges', visualize_fps(edges, fps))
                #cv2.imshow('Edges 50', visualize_fps(edges_50, fps))
                
                if frame_gray_p is not None:
                    if mse(frame_gray, frame_gray_p) > MSE_THRESHOLD:
                        print('Frame {0}: Motion Detected!'.format(cnt_frame))
                
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
        cap.release()
        cv2.destroyAllWindows()
