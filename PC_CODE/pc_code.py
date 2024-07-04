import subprocess
import os

# Replace 'file1.py' and 'file2.py' with the actual file names you want to execute
file1 = 'server.py'
file2 = 'from_csv_to_jpg.py'
file3 = 'counter.py'

# Execute file1.py
#subprocess.run(['python', file1])

# Correct usage of os.devnull to suppress output
with open(os.devnull, 'w') as devnull:
    subprocess.run(['python', file1])
    subprocess.run(['python', file2], stdout=devnull, stderr=devnull)
    subprocess.run(['python', file3], stdout=devnull,  stderr=devnull)

# Execute file2.py
#subprocess.run(['python', file2], stdout=os.devnull,  stderr=os.devnull)

# Execute file3.py
#subprocess.run(['python', file3], stdout=os.devnull,  stderr=os.devnull)