import socket
import curses
import time
import threading
import math

# Configuration
ESP_DEVICES = {
    "192.168.1.92": 30,  # ESP1 desktop
    "192.168.1.72": 300,  # ESP2 A4 panel
    # Add more ESPs as needed
}
ESP_PORT = 6455
ARTNET_PORT = 6454
UNIVERSE_SIZE = 512  # DMX channels per universe
LEDS_PER_UNIVERSE = 170  # 170 LEDs per universe (since each LED uses 3 channels)

# Calculate universe allocation
esp_universe_map = {}  # {universe: (esp_ip, led_offset)}
esp_expected_universes = {}  # {esp_ip: number_of_universes}
esp_data_buffer = {}  # {esp_ip: bytearray(led_data)}
esp_received_universes = {}  # {esp_ip: set(received_universe_ids)}

universe_index = 0
for esp_ip, led_count in ESP_DEVICES.items():
    needed_universes = math.ceil(led_count / LEDS_PER_UNIVERSE)  # Always round up
    esp_expected_universes[esp_ip] = needed_universes
    esp_data_buffer[esp_ip] = bytearray([0] * (needed_universes * LEDS_PER_UNIVERSE * 3))
    esp_received_universes[esp_ip] = set()  # Track universes received for this ESP

    for i in range(needed_universes):
        esp_universe_map[universe_index] = (esp_ip, i * LEDS_PER_UNIVERSE * 3)
        universe_index += 1

# Create Art-Net and UDP sockets
artnet_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
artnet_sock.bind(("0.0.0.0", ARTNET_PORT))

esp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Function to process Art-Net data
def process_artnet_data(data, addr):
    if len(data) < 18 or not data.startswith(b"Art-Net\0"):
        return
    
    universe = data[14] | (data[15] << 8)
    if universe not in esp_universe_map:
        return  # Ignore irrelevant universes
    
    dmx_data = data[18:18 + UNIVERSE_SIZE]
    
    esp_ip, led_offset = esp_universe_map[universe]
    esp_data_buffer[esp_ip][led_offset:led_offset + len(dmx_data)] = dmx_data
    esp_received_universes[esp_ip].add(universe)
    
    # Check if all universes for this ESP are received
    if len(esp_received_universes[esp_ip]) == esp_expected_universes[esp_ip]:
        esp_sock.sendto(esp_data_buffer[esp_ip], (esp_ip, ESP_PORT))
        esp_received_universes[esp_ip].clear()  # Reset for next frame

# Function to listen for Art-Net packets
def artnet_listener():
    while True:
        try:
            data, addr = artnet_sock.recvfrom(1024)
            process_artnet_data(data, addr)
        except Exception:
            pass  # Ignore errors to keep running

# Function for CLI interface
def cli_interface(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Art-Net Universe Status")
        stdscr.addstr(1, 0, "=" * 40)
        
        row = 3
        for esp_ip, expected_count in esp_expected_universes.items():
            received_count = len(esp_received_universes[esp_ip])
            status = f"Waiting ({received_count}/{expected_count})" if received_count < expected_count else "Sent"
            stdscr.addstr(row, 0, f"{esp_ip}: {status}")
            row += 1
        
        stdscr.refresh()
        time.sleep(0.5)

# Start Art-Net listener thread
artnet_thread = threading.Thread(target=artnet_listener, daemon=True)
artnet_thread.start()

# Start CLI interface
curses.wrapper(cli_interface)
