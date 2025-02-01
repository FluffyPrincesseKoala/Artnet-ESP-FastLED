import socket
import struct
import time

# ESP8266 IP and port
ESP_IP = "192.168.1.92"
# ESP_IP = "192.168.1.72"
ESP_PORT = 6455

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(0.5)  # Set timeout for acknowledgment

# Function to send binary LED data
def send_led_data_binary(led_data, retries=3):
    for attempt in range(retries):
        try:
            sock.sendto(led_data, (ESP_IP, ESP_PORT))
            print(f"Sent binary data (Attempt {attempt + 1})")
            # Wait for acknowledgment
            ack = sock.recv(1024).decode()
            if ack == "ACK":
                print("Acknowledgment received.")
                return True
        except socket.timeout:
            print("No acknowledgment received.")
        except Exception as e:
            print(f"Error sending data: {e}")
    return False

# Prepare binary LED data (300 LEDs, alternating red and green)
num_leds = 300
led_data = bytearray()
for i in range(num_leds):
    # led_data.extend([0, 0, 0]) # RGB values for each LED
    
    # if i % 2 == 0:  # Red
    #     led_data.extend([255, 0, 0])
    # else:  # Green
    #     led_data.extend([0, 255, 0])

    led_data.extend(
        [
            int(32 * ((1 + i) % 3 == 0)),
            int(32 * ((1 + i) % 3 == 1)),
            int(32 * ((1 + i) % 3 == 2)),
        ]
    )

# Send the binary data
if not send_led_data_binary(led_data):
    print("Failed to send LED data.")

# Close the socket
sock.close()
