import socket
import time
import os
from datetime import datetime, timedelta

# def is_within_active_period(start_hour=8, end_hour=19):
#     now = datetime.now()
#     start_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
#     end_time = now.replace(hour=end_hour, minute=0, second=0, microsecond=0)
#     return start_time <= now <= end_time

# def time_until_next_active_period(start_hour=8):
#     now = datetime.now()
#     next_start_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
#     if now > next_start_time:
#         next_start_time += timedelta(days=1)
#     return (next_start_time - now).total_seconds()

def send_all(sock, data):
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError('Socket connection broken')
        total_sent += sent

folder_path = 'images/'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (('80.182.230.135', 2000))  # Use the IP address of the VM
server_address = (('192.168.1.100', 2000))  # Use the IP address of the VM
server_address = (('157.27.138.33', 2000))  # Use the IP address of the VM
client_socket.connect(server_address)

#message = 'Hello, server!'
#client_socket.sendall(message.encode())
# Specify the file to be sent
#file_name = '2024_05_27__11_34_00.jpg'

while True:
    folder_contents = os.listdir(folder_path)
    folder_contents = sorted(folder_contents)
    #print(len(folder_contents))
    if len(folder_contents) != 0:
        file_name = folder_contents[0]

        # Send the length of the file name
        client_socket.sendall(str(len(file_name)).zfill(4).encode('utf-8'))

        # Send the file name
        client_socket.sendall(file_name.encode('utf-8'))

        file_path = 'images/' + file_name
        # Open the image file in binary mode
        with open(file_path, 'rb') as file:
            image_data = file.read()

        send_all(client_socket, image_data)
        print('Image {} data sent to server'.format(file_name), flush=True)

        client_socket.sendall(b'@END@')

        # with open('/home/univr/Desktop/images/' + file_name, 'rb') as f:
        #     while True:
        #         chunk = f.read(1024)
        #         if not chunk:
        #             break
        #         client_socket.sendall(chunk)

        confirmation = client_socket.recv(1024)
        if confirmation.decode('utf-8') == 'Image received successfully':
            os.remove(file_path)
            print('Server confirmed image reception. Image file delete...')
        
        file_extension = os.path.splitext(file_name)[1].lower()
        if file_extension == '.csv':
            break
        #time.sleep(1)
    
    #if not(is_within_active_period()):    
    #    print("Process paused. Waiting until 8 AM...")
    #    sleep_time = time_until_next_active_period()
    #    time.sleep(sleep_time)
        
# Close the connection
client_socket.close()
