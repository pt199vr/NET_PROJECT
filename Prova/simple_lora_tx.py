from pyLoraRFM9x import LoRa, ModemConfig
import time
from PIL import Image
import io


# This is our callback function that runs when a message is received
def on_recv(payload):
    print("From:", payload.header_from)
    print("Received:", payload.message)
    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))


if __name__ == "__main__":
    
    lora = LoRa(spi_channel=1, interrupt_pin=5, my_address=1, spi_port=0, reset_pin = 25, freq=434.0, tx_power=20, modem_config=ModemConfig.Bw125Cr45Sf128, acks=True)
     
    #lora.on_recv = on_recv
    
    #lora.set_mode_tx()
    lora.set_mode_rx()
    
    # Send a message to a recipient device with address 10
    # Retry sending the message twice if we don't get an  acknowledgment from the recipient
    message = 'Hello world!'
    while(True):
        time.sleep(1)
        status = lora.send_to_wait(message, 5, retries=3) 
        print(status)
        if status:
            print("Sent")
        else:
            print("No")
        
        
