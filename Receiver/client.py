import socket
import time
import os
from datetime import datetime, timedelta

def send_all(sock, data):
    total_sent = 0
    while total_sent < len(data):
        sent = sock.send(data[total_sent:])
        if sent == 0:
            raise RuntimeError('Socket connection broken')
        total_sent += sent

folder_path = 'images/'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = (('157.27.136.184', 6000))  
client_socket.connect(server_address)


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

        confirmation = client_socket.recv(1024)
        if confirmation.decode('utf-8') == 'Image received successfully':
            os.remove(file_path)
            print('Server confirmed image reception. Image file delete...')
        
        file_extension = os.path.splitext(file_name)[1].lower()

    else:
        file_name = 'Bye-bye'
        # Send the length of the file name
        client_socket.sendall(str(len(file_name)).zfill(4).encode('utf-8'))
        
        client_socket.sendall(file_name.encode('utf-8'))
        break
        
# Close the connection
client_socket.close()
