import socket

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_address = ('192.168.1.107', 8080)
server_socket.bind(server_address)

# Listen for incoming connections
server_socket.listen(1)

print('Waiting for a connection...')

# Accept a connection
client_socket, client_address = server_socket.accept()

print('Connection established with', client_address)

# Receive data from the client
data = client_socket.recv(1024)
print('Received:', data.decode())

# Receive the image data from the client
image_data = b''
while True:
    chunk = client_socket.recv(1024)
    if not chunk:
        break
    image_data += chunk

# Save the received image data to a file
with open('received_image.jpg', 'wb') as f:
    f.write(image_data)
    print('Image received and saved as "received_image.jpg"')

# Close the connection
client_socket.close()