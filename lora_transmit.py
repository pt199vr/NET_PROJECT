import time
from pyLoraRFM9x import LoRa, Modulation

# Configure LoRa parameters
spi_bus = 0
cs_pin = 0
reset_pin = 25
frequency = 915.0  # Frequency in MHz (adjust according to your module)

# Initialize LoRa module
lora = LoRa(spi_bus, cs_pin, reset_pin, frequency)
lora.set_modulation(Modulation.LORA)
lora.set_tx_power(20)  # Set transmission power

# Send a test message
message = "Hello, LoRa!"
print(f"Sending message: {message}")
lora.send(message.encode())

# Wait for a bit to ensure the message is sent
time.sleep(2)

print("Message sent successfully!")
