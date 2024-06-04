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
file_path = ""

# This is our callback function that runs when a message is received
def on_recv(payload):
    print("From:", payload.header_from)
    print("Received:", payload.message)
    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))
    
    global flag
    if payload.message == b'OK':
        flag = True
        os.remove(file_path)
        print('Server confirmed image reception. Image file delete...')
    else:
        flag = False

if __name__ == "__main__":
    
    folder_path = '/home/univr/Desktop/images/'    
    lora = LoRa(spi_channel=1, interrupt_pin=5, my_address=5, spi_port=0, reset_pin = 25, freq=434.0, tx_power=14, modem_config=ModemConfig.Bw125Cr45Sf128, acks=True)
    #lora.retry_timeout = 2
     
    lora.on_recv = on_recv    
    lora.set_mode_tx()
    
    while True:
        while True:
            
            folder_contents = os.listdir(folder_path)            
            print(folder_contents)          
            if len(folder_contents) == 0:
                break
                
            file_name = folder_contents[-1]
            print(file_name)
            
            file_path = folder_path + file_name
            
            byte = ('@NAME@'+file_name).encode()
            print(byte)
            
            status = lora.send_to_wait(byte, 0, retries=0) 

            load_image(file_path)
            lora.set_mode_rx()
            
            while True:
                print(".")
                time.sleep(1)
                if flag:
                    #i = i+1
                    break
                    
            flag = False
            lora.set_mode_tx()
        time.sleep(60)
