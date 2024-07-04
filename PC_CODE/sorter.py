import os
import shutil

# Directory containing the files
folder_path = 'INSETTI'

# Function to extract date and fototrappola from file name
def extract_info(filename):
    parts = filename.split('_')
    date_str = '_'.join(parts[3:6])  # Extracts the date part from the file name
    fototrappola = parts[0]  # Extracts the fototrappola identifier
    return date_str, fototrappola

# List all files in the directory
files = os.listdir(folder_path)

for file in files:
    # Extract date and fototrappola from file name
    date_str, fototrappola = extract_info(file)
    
    # Create a new folder path for the date
    date_folder_path = os.path.join(folder_path, date_str)
    
    # Create a new folder path for the fototrappola inside the date folder
    fototrappola_folder_path = os.path.join(date_folder_path, fototrappola)
    
    # Check if the date folder exists, if not create it
    if not os.path.exists(date_folder_path):
        os.makedirs(date_folder_path)
    
    # Check if the fototrappola folder exists, if not create it
    if not os.path.exists(fototrappola_folder_path):
        os.makedirs(fototrappola_folder_path)
    
    # Move the file to the fototrappola folder inside the date folder
    shutil.move(os.path.join(folder_path, file), os.path.join(fototrappola_folder_path, file))