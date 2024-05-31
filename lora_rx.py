from pyLoraRFM9x import LoRa, ModemConfig
import time
from PIL import Image
import io

current_image = b''
received = 0

# This is our callback function that runs when a message is received
def on_recv(payload):
    global current_image
    global received
    
    #print("From:", payload.header_from)
    #print("Received:", payload.message)
    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))
    
    if(payload.message == b'@END@'):
        with open("jhgf.jpg", "wb") as i:
            i.write(current_image)
            print("Image saved lmaooo, " + str(received) + "packets.")
    elif(payload.message == "@START@"):
        current_image = b''
    else:  
        current_image += payload.message
        received += 1

if __name__ == "__main__":
    
    # Lora object will use spi port 0 and use chip select 1. GPIO pin 5 will be used for interrupts and set reset pin to 25
    # The address of this device will be set to 2
    lora = LoRa(spi_channel=1, interrupt_pin=5, my_address=0, spi_port=0, reset_pin = 25, freq=434.0, tx_power=14, modem_config=ModemConfig.Bw125Cr45Sf128, acks=True)
     
    lora.on_recv = on_recv
    
    lora.set_mode_rx()

    while(True):
        time.sleep(1)
        print(".")
        
# Send a message to a recipient device with address 10
# Retry sending the message twice if we don't get an  acknowledgment from the recipient
#message = "Hello there!"
#status = lora.send_to_wait(message, 10, retries=2)
#if status is True:
#    print("Message sent!"
#else:
#    print("No acknowledgment from recipient")


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
