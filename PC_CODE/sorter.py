import os
import shutil

# Directory containing the files
folder_path = 'INSETTI/'

# Function to extract date from file name
def extract_date(filename):
    # Assuming the date is always in the format "YYYY_MM_DD" and at the same position in the file name
    parts = filename.split('_')
    date_str = '_'.join(parts[3:6])  # Extracts the date part from the file name
    return date_str

# List all files in the directory
files = os.listdir(folder_path)

for file in files:
    # Extract date from file name
    date_str = extract_date(file)
    
    # Create a new folder path for the date
    new_folder_path = os.path.join(folder_path, date_str)
    
    # Check if the folder exists, if not create it
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    
    # Move the file to the new folder
    shutil.move(os.path.join(folder_path, file), os.path.join(new_folder_path, file))