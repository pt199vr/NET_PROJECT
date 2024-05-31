from pyLoraRFM9x import LoRa, ModemConfig
import time
from PIL import Image
import io
import os


def load_image(image_name):
    
    with open(image_name, "rb") as image_file:
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
        #while not(status):
        #    status = lora.send_to_wait(chunk, 0, retries=0)
        #    print("Re-send package")
        
        # Here you can process each chunk as needed
        print(f"Processing chunk {i+1}/{num_chunks}: {chunk[:10]}...")  
        
        time.sleep(0.05)
        
    status = lora.send_to_wait(b'@END@', 0, retries=0) 
    #while not(status):
     #    print("aiuto")
     #   status = lora.send_to_wait(b'@END@', 0, retries=0)
    
    print("End sent")
       
flag = False
# This is our callback function that runs when a message is received
def on_recv(payload):
    print("From:", payload.header_from)
    print("Received:", payload.message)
    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))
    
    global flag
    if payload.message == b'OK':
        flag = True
    else:
        flag = False


if __name__ == "__main__":
    folder_path = '/home/univr/Desktop/images/'
    
    # Lora object will use spi port 0 and use chip select 1. GPIO pin 5 will be used for interrupts and set reset pin to 25
    # The address of this device will be set to 2
    lora = LoRa(spi_channel=1, interrupt_pin=5, my_address=5, spi_port=0, reset_pin = 25, freq=434.0, tx_power=14, modem_config=ModemConfig.Bw125Cr45Sf128, acks=True)
    #lora.retry_timeout = 2
     
    lora.on_recv = on_recv
    
    lora.set_mode_tx()
    
    # Send a message to a recipient device with address 10
    # Retry sending the message twice if we don't get an  acknowledgment from the recipient
    
    #while(True):
    #time.sleep(1)
    #for i in range(10):
    folder_contents = os.listdir(folder_path)
    #print(len(folder_contents))
    i = 0
    while True:
        if len(folder_contents) != 0:
            file_name = folder_contents[i]
            print(folder_contents)
            
            byte = ('@NAME@'+file_name).encode()
            print(byte)
            status = lora.send_to_wait(byte, 0, retries=0) 
            #while not(status):
            #    status = lora.send_to_wait(byte, 0, retries=0)
            
            print(file_name)
            
            file_path = '/home/univr/Desktop/images/' + file_name
            load_image(file_path)
            lora.set_mode_rx()
            
            while True:
                print(".")
                time.sleep(1)
                if flag:
                    i = i+1
                    break
                    
            flag = False
            lora.set_mode_tx()
            #print(len(message))
            
