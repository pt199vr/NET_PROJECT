import subprocess
import os

# Replace 'file1.py' and 'file2.py' with the actual file names you want to execute
server = 'server.py'
sorter = 'sorter.py'
transf = 'from_csv_to_jpg.py'
count = 'counter.py'

# Execute file1.py
#subprocess.run(['python', file1])

# Correct usage of os.devnull to suppress output
with open(os.devnull, 'w') as devnull:
    #subprocess.run(['python', server])
    subprocess.run(['python', sorter])
    subprocess.run(['python', transf])    
    subprocess.run(['python', count])

# Execute file2.py
#subprocess.run(['python', file2], stdout=os.devnull,  stderr=os.devnull)

# Execute file3.py
#subprocess.run(['python', file3], stdout=os.devnull,  stderr=os.devnull)