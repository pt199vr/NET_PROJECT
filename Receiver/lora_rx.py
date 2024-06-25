from pyLoraRFM9x import LoRa, ModemConfig
import time
from PIL import Image
import io

current_image = b''
received = 0
file_name = ""


def is_image_corrupted(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()  # Verify if it is, in fact, an image
        return False
    except (IOError, SyntaxError) as e:
        print(f"Image is corrupted: {e}")
        return True
        
def on_recv(payload):
    global current_image
    global received
    global file_name
    #lora.set_mode_rx()
    
    #print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))
    #print(payload.message)
            
    if(payload.message == b'@END@'):
        lora.set_mode_tx()
        with open(file_name, "wb") as i:
            i.write(current_image)
            print("Image saved, " + str(received) + "packets.")
        received = 0
        current_image = b''
        #lora.send_ack(1, header_id = payload.header_id)
        
        if not(is_image_corrupted(file_name)):
            print("Success")
            lora.send_to_wait(b'OK', 5, retries = 0)
        else:
            print(file_name + " img corrupted")
            lora.send_to_wait(b'NO', 5, retries = 0)
        lora.set_mode_rx()
        
    elif(payload.message.startswith(b'@NAME')):
        file_name = payload.message.decode("utf-8").split("@")[2]
        print(file_name)
    else:  
        current_image += payload.message
        received += 1
        
    
if __name__ == "__main__":
    
    lora = LoRa(spi_channel=1, interrupt_pin=5, my_address=0, spi_port=0, reset_pin = 25, freq=434.0, tx_power=14, modem_config=ModemConfig.Bw125Cr45Sf128, acks=True)
     
    lora.on_recv = on_recv
    
    lora.set_mode_rx()

    while(True):
        time.sleep(1)
        print(".")
        
