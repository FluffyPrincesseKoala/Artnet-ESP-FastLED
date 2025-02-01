#include <FastLED.h>
#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

// LED Configuration
#define DATA_PIN_1 4 // Pin for the first strip
#define DATA_PIN_2 5 // Pin for the second strip
#define NUM_LEDS_PER_STRIP 720
#define BRIGHTNESS 255
#define LED_TYPE WS2812B
#define COLOR_ORDER GRB

CRGB leds_1[NUM_LEDS_PER_STRIP];
// CRGB leds_2[NUM_LEDS_PER_STRIP];

// WiFi Configuration
const char *ssid = "Freebox-686A2A";
const char *password = "2kkKaym#";

WiFiUDP udp;
unsigned int udp_port = 6455;
const int PACKET_SIZE = 2161;     // 434;  // 50 LEDs per packet (50 * 3 = 150 bytes)
char incomingPacket[PACKET_SIZE]; // Buffer for incoming UDP packets

void setup()
{
  // Initialize LEDs
  FastLED.addLeds<LED_TYPE, DATA_PIN_1, COLOR_ORDER>(leds_1, NUM_LEDS_PER_STRIP);
  // FastLED.addLeds<LED_TYPE, DATA_PIN_2, COLOR_ORDER>(leds_2, NUM_LEDS_PER_STRIP);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.clear();
  FastLED.show();

  // Initialize Serial Monitor
  Serial.begin(115200);
  Serial.println("Starting ESP8266...");

  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("WiFi connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Start UDP
  udp.begin(udp_port);
  Serial.printf("Listening on UDP port %d\n", udp_port);
}

void loop()
{
  int packetSize = udp.parsePacket();
  if (packetSize)
  {
    Serial.printf("Packet received, size: %d bytes\n", packetSize);
    int len = udp.read(incomingPacket, sizeof(incomingPacket) - 1);
    if (len > 0)
    {
      incomingPacket[len] = '\0'; // Null-terminate the received data
      parse_binary_colors((uint8_t *)incomingPacket, len);
      udp.beginPacket(udp.remoteIP(), udp.remotePort());
      udp.write("ACK");
      udp.endPacket();
    }
    else
    {
      Serial.println("Failed to read UDP packet.");
    }
  }
}

void parse_binary_colors(uint8_t *data, int len)
{
  for (int i = 0; i < len / 3 && i < NUM_LEDS_PER_STRIP * 2; i++)
  {
    // if (i < NUM_LEDS_PER_STRIP)
    // {
    leds_1[i] = CRGB(data[i * 3], data[i * 3 + 1], data[i * 3 + 2]);
    // }
    // else
    // {
    //   leds_2[i - NUM_LEDS_PER_STRIP] = CRGB(data[i * 3], data[i * 3 + 1], data[i * 3 + 2]);
    // }
  }
  FastLED.show();
  Serial.println("LEDs updated.");
}
