from pyLoraRFM9x import LoRa, ModemConfig
import time
from PIL import Image
import io

def on_recv(payload):
    print("From:", payload.header_from)
    print("Received:", payload.message)
    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))
    #lora.send_ack(1, header_id = payload.header_id)
    lora.set_mode_rx()
	
if __name__ == "__main__":
  
    lora = LoRa(spi_channel=1, interrupt_pin=5, my_address=5, spi_port=0, reset_pin = 25, freq=434.0, tx_power=20, modem_config=ModemConfig.Bw125Cr45Sf128, acks=True)
     
    lora.on_recv = on_recv
    
    lora.set_mode_rx()
    while True:
        print(".")
        time.sleep(1)			
