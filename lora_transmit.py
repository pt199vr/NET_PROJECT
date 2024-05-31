from pyLoraRFM9x import LoRa, ModemConfig
import time
from PIL import Image
import io


def load_image():
    with open("image1.jpg", "rb") as image_file:
        byte_array = image_file.read()
    
    # Process the image file in chunks of 250 bytes
    chunk_size = 250
    num_chunks = (len(byte_array) + chunk_size - 1) // chunk_size  
    
    for i in range(num_chunks):
        start = i * chunk_size
        end = start + chunk_size
        
        if end > len(byte_array):
                end = len(byte_array)
                
        chunk = byte_array[start:end]
        status = lora.send_to_wait(chunk, 0, retries=0) 
        # Here you can process each chunk as needed
        print(f"Processing chunk {i+1}/{num_chunks}: {chunk[:10]}...")  
        
        time.sleep(1)
    status = lora.send_to_wait(b'@END@', 0, retries=0) 

# This is our callback function that runs when a message is received
def on_recv(payload):
    print("From:", payload.header_from)
    print("Received:", payload.message)
    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))


if __name__ == "__main__":
    
    # Lora object will use spi port 0 and use chip select 1. GPIO pin 5 will be used for interrupts and set reset pin to 25
    # The address of this device will be set to 2
    lora = LoRa(spi_channel=1, interrupt_pin=5, my_address=1, spi_port=0, reset_pin = 25, freq=434.0, tx_power=14, modem_config=ModemConfig.Bw125Cr45Sf128, acks=True)
     
    #lora.on_recv = on_recv
    
    lora.set_mode_tx()
    
    # Send a message to a recipient device with address 10
    # Retry sending the message twice if we don't get an  acknowledgment from the recipient
    
    #while(True):
    #time.sleep(1)
    load_image()
        #print(len(message))
            



# import time
# from pyLoraRFM9x import LoRa, Modulation

# # Configure LoRa parameters
# spi_bus = 0
# cs_pin = 0
# reset_pin = 25
# frequency = 915.0  # Frequency in MHz (adjust according to your module)

# # Initialize LoRa module
# lora = LoRa(spi_bus, cs_pin, reset_pin, frequency)
# lora.set_modulation(Modulation.LORA)
# lora.set_tx_power(20)  # Set transmission power

# # Send a test message
# message = "Hello, LoRa!"
# print(f"Sending message: {message}")
# lora.send(message.encode())

# # Wait for a bit to ensure the message is sent
# time.sleep(2)

# print("Message sent successfully!")
