import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (('79.17.241.26', 2000))  # Use the IP address of the VM
client_socket.connect(server_address)

message = 'Hello, server!'
client_socket.sendall(message.encode())

# Open the image file in binary mode
with open('received_image.jpg', 'rb') as file:
    image_data = file.read()

# Send the image data to the client
client_socket.sendall(image_data)

print('Image sent to client\n')

# Send a response back to the client
#client_socket.sendall(b'Image send successfully!')

# Close the connection
client_socket.close()
