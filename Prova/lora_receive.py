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

print("Waiting for a message...")

while True:
    if lora.received():
        message = lora.receive().decode()
        print(f"Received message: {message}")
    time.sleep(1)
