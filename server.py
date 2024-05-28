import socket
import sys

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
server_address = ('192.168.1.62', 2000)
server_address = ('192.168.1.100', 2000)
#server_address = ('157.27.145.15', 2000)
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
        #print('File name length received:', file_name_length)

        # Now, receive the file name itself
        file_name = client_socket.recv(file_name_length).decode('utf-8')
        #print('File name received:', file_name)

        # Receive data from the client
        #data = client_socket.recv(1024)
        #print('Received:', data.decode())

        # Receive the image data from the client
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
                #print(f'Received {len(chunk)} bytes, total {len(image_data)} bytes', flush=True)
        
        #print(image_data)
        end_pos = image_data.find(b'@END@')
        # Save the received image data to a file
        if end_pos != -1:
                # If delimiter is found, truncate the image data at the delimiter position
                with open(file_name, 'wb') as f:
                    f.write(image_data[:end_pos])
                    print(f'Image received and saved as "{file_name}"', flush=True)
        else:
                # If delimiter is not found, save the entire image data
                with open(file_name, 'wb') as f:
                    f.write(image_data)
                    print(f'Image received and saved as "{file_name}"', flush=True)
        
        if not(is_image_corrupted(file_name)):
            #sys.stdout.flush()
            client_socket.sendall('Image received successfully'.encode())
        else:
            print(file_name + " img corrupted")
            client_socket.sendall('Not successfully'.encode())
finally:
    # Close the connection
    client_socket.close()
    server_socket.close()
