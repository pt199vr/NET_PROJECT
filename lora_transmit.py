from pyLoraRFM9x import LoRa, ModemConfig

# This is our callback function that runs when a message is received
def on_recv(payload):
    print("From:", payload.header_from)
    print("Received:", payload.message)
    print("RSSI: {}; SNR: {}".format(payload.rssi, payload.snr))

# Lora object will use spi port 0 and use chip select 1. GPIO pin 5 will be used for interrupts and set reset pin to 25
# The address of this device will be set to 2
lora = LoRa(0, 1, 5, 2, reset_pin = 25, modem_config=ModemConfig.Bw125Cr45Sf128, tx_power=14, acks=True)
lora.on_recv = on_recv

# Send a message to a recipient device with address 10
# Retry sending the message twice if we don't get an  acknowledgment from the recipient
message = "Hello there!"
status = lora.send_to_wait(message, 10, retries=2)
if status is True:
    print("Message sent!")
else:
    print("No acknowledgment from recipient")


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
