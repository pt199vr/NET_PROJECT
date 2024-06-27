import socket
import sys
import os

from PIL import Image

def is_image_corrupted(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()  # Verify if it is, in fact, an image
        return False
    except (IOError, SyntaxError) as e:
        print(f"Image is corrupted: {e}")
        return True
    
# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = ('157.27.131.166', 2000)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print('Waiting for a connection...')

# Accept a connection
client_socket, client_address = server_socket.accept()

print('Connection established with', client_address)

try:
    while True:
        # First, receive the file name length
        file_name_length = int(client_socket.recv(4).decode('utf-8'))

        # Now, receive the file name itself
        file_name = client_socket.recv(file_name_length).decode('utf-8')

        file_extension = os.path.splitext(file_name)[1].lower()
        image_data = b''
        while True:
                chunk = client_socket.recv(1024)
                if chunk == b'@END@':
                    break
                if chunk.endswith(b'@END@'):
                    image_data += chunk
                    #print(image_data)
                    break
                image_data += chunk
        
        #print(image_data)
        end_pos = image_data.find(b'@END@')
        if file_extension == '.csv':
            # Open the CSV file in binary mode and send it
            data = image_data
            with open('output.csv', 'wb') as file:
                csv_data = file.write(data)
            print('CSV file {} data sent to server'.format(file_name), flush=True)
            client_socket.sendall('Image received successfully'.encode())
            break
        else:
            # Save the received image data to a file
            fname = os.path.join('INSETTI', file_name)
            print(file_name)
            if end_pos != -1:
                    # If delimiter is found, truncate the image data at the delimiter position
                    with open(fname, 'wb') as f:
                        f.write(image_data[:end_pos])
                        print(f'Image received and saved as "{fname}"', flush=True)
            else:
                    # If delimiter is not found, save the entire image data
                    with open(fname, 'wb') as f:
                        f.write(image_data)
                        print(f'Image received and saved as "{fname}"', flush=True)
            
            if not(is_image_corrupted(fname)):
                #sys.stdout.flush()
                client_socket.sendall('Image received successfully'.encode())
            else:
                print(fname + " img corrupted")
                client_socket.sendall('Not successfully'.encode())

finally:
    # Close the connection
    client_socket.close()
    server_socket.close()
