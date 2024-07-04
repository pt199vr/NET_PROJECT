import cv2
import os
import numpy as np
import csv
from PIL import Image
from infer import inference
import shutil

class_labels = [
        'ant',
        'bee',
        'bee_apis',
        'bee_bombus',
        'beetle',
        'beetle_cocci',
        'beetle_oedem',
        'bug',
        'bug_grapho',
        'fly',
        'fly_empi',
        'fly_sarco',
        'fly_small',
        'hfly_episyr',
        'hfly_eristal',
        'hfly_eupeo',
        'hfly_myathr',
        'hfly_sphaero',
        'hfly_syrphus',
        'lepi',
        'none_background',
        'none_bird',
        'none_dirt',
        'none_shadow',
        'other',
        'scorpionfly',
        'wasp'
    ]

def counter(lst, str):
    if str in lst:
        lst[str] += 1
    else:
        lst[str] = 1

path_to_source = 'INSETTI/'
path_to_collage = 'COLLAGE/'
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 768

dict = {}

image = np.ones((IMAGE_HEIGHT, IMAGE_WIDTH, 3), np.uint8) * 255
csv_file = 'classification.csv'

dest_path = 'classified/'
csv_file = 'classification.csv'
csv_file_res = 'results.csv'
file_exists = os.path.isfile(csv_file)
file_exists_res = os.path.isfile('results.csv')
file =  open(csv_file, mode='a', newline='')
file_res =  open(csv_file_res, mode='a', newline='')
writer = csv.writer(file)
res = csv.writer(file_res)
if not file_exists:
        writer.writerow(['Frame','ImageName', 'Class'])
if not file_exists_res:
        t = ['Frame'] + class_labels + ['Total']
        res.writerow(t)       
# Read the CSV file
with open('output.csv', 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    current_frame_id = 0

    # Loop through each row in the CSV file
    for row in csv_reader:
        image_filename = row[0]
        image_path = os.path.join(path_to_source, image_filename)
        
        if not os.path.exists(image_path):
            continue

        classification = inference(image_path)
        writer.writerow([current_frame_id, image_filename, classification]) 
        dir_path = dest_path + classification
        if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        temp_str = dir_path + '/' + image_filename
        shutil.copy2(image_path, temp_str)

        current_frame = cv2.imread(image_path)        
        if current_frame is None:
            continue

        object_id = int(row[1])
        if current_frame_id != object_id:
            
            s = []
            tot = 0
            for elem in class_labels:
                if elem in dict.keys():
                    s.append(dict[elem])
                    tot += dict[elem]
                else:
                    s.append(0) 
            s.append(tot)   
            dict = {}
            res.writerow([current_frame_id] + s)    
            cv2.imwrite(os.path.join(path_to_collage, str(current_frame_id) + '.jpg'), image)
            image[:] = (255, 255, 255)
            current_frame_id = object_id
       
        # Check if the object ID matches the current frame ID
        if object_id == current_frame_id:
            # Paste the current frame onto the image
            x, y, w, h = int(row[3]), int(row[4]), int(row[5]), int(row[6])
            h = current_frame.shape[0]
            w = current_frame.shape[1]
            print(current_frame.shape, image_path, x, y, w, h)
            image[y:y+h, x:x+w] = current_frame
            counter(dict, classification)


            
                       
            
            
