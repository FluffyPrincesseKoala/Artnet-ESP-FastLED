import socket

# Configuration
# ESP_IP = "192.168.1.72"
ESP_IP = "192.168.1.92"
ESP_PORT = 6455
ARTNET_PORT = 6454
UNIVERSE_SIZE = 512  # DMX channels per universe
LEDS_PER_UNIVERSE = 170  # Each LED uses 3 channels (RGB)
TOTAL_LEDS = 30  # Total LEDs to control
TOTAL_UNIVERSES = (TOTAL_LEDS + LEDS_PER_UNIVERSE - 1) // LEDS_PER_UNIVERSE

# Create Art-Net and UDP sockets
artnet_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
artnet_sock.bind(("0.0.0.0", ARTNET_PORT))

esp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Create an array to store LED states
led_states = bytearray([0] * (TOTAL_LEDS * 3))

# Function to process Art-Net data and map to LEDs
def process_artnet_data(data):
    if len(data) < 18:
        return None

    # Extract universe number (bytes 14-15)
    universe = data[14] | (data[15] << 8)
    print(f"Universe: {universe}")

    # Map the universe to the correct LED range
    start_led = universe * LEDS_PER_UNIVERSE
    if start_led >= TOTAL_LEDS:
        print(f"Universe {universe} out of range. Ignored.")
        return None

    # Extract DMX data
    dmx_data = data[18:18 + UNIVERSE_SIZE]

    # Update the corresponding LED range
    for i in range(LEDS_PER_UNIVERSE):
        if start_led + i < TOTAL_LEDS:
            r = dmx_data[i * 3] if i * 3 < len(dmx_data) else 0
            g = dmx_data[i * 3 + 1] if i * 3 + 1 < len(dmx_data) else 0
            b = dmx_data[i * 3 + 2] if i * 3 + 2 < len(dmx_data) else 0
            led_states[(start_led + i) * 3:(start_led + i) * 3 + 3] = [r, g, b]

print("Listening for Art-Net data...")

while True:
    try:
        # Receive Art-Net data
        data, addr = artnet_sock.recvfrom(1024)
        if data.startswith(b"Art-Net\0"):
            print(f"Art-Net packet received from {addr}")

            # Process the Art-Net data
            process_artnet_data(data)

            # Send the updated LED data to ESP8266
            esp_sock.sendto(led_states, (ESP_IP, ESP_PORT))
            print(f"LED data sent to ESP8266: {len(led_states)} bytes")
    except Exception as e:
        print(f"Error: {e}")
