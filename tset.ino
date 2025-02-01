// #include <FastLED.h>
// #include <ESP8266WiFi.h>
// #include <WiFiUdp.h>

// // LED Configuration
// #define DATA_PIN 4  // D2 on the ESP8266
// #define NUM_LEDS 30 // Number of LEDs in your strip
// #define BRIGHTNESS 128
// #define LED_TYPE WS2812B
// #define COLOR_ORDER GRB

// CRGB leds[NUM_LEDS];

// // WiFi Configuration
// const char *ssid = "Freebox-686A2A"; // Replace with your WiFi SSID
// const char *password = "2kkKaym#";   // Replace with your WiFi password

// WiFiUDP udp;
// unsigned int udp_port = 6455; // UDP port to listen on
// char incomingPacket[1024];    // Buffer for incoming UDP packets

// void setup()
// {
//     // Initialize LEDs
//     FastLED.addLeds<LED_TYPE, DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS);
//     FastLED.setBrightness(BRIGHTNESS);
//     FastLED.clear();
//     FastLED.show();

//     // Initialize Serial Monitor
//     Serial.begin(115200);
//     delay(10);

//     // Connect to WiFi
//     Serial.println("Connecting to WiFi...");
//     WiFi.begin(ssid, password);

//     while (WiFi.status() != WL_CONNECTED)
//     {
//         delay(1000);
//         Serial.println("Connecting...");
//     }

//     Serial.println("WiFi connected!");
//     Serial.print("IP Address: ");
//     Serial.println(WiFi.localIP());

//     // Start UDP
//     udp.begin(udp_port);
//     Serial.printf("Listening for UDP packets on port %d\n", udp_port);
// }

// void loop()
// {
//     // Check for incoming UDP packets
//     int packetSize = udp.parsePacket();
//     if (packetSize)
//     {
//         int len = udp.read(incomingPacket, sizeof(incomingPacket) - 1);
//         if (len > 0)
//         {
//             incomingPacket[len] = '\0'; // Null-terminate the received data
//             parseAndSetLEDs(incomingPacket);
//         }
//     }
// }

// void parseAndSetLEDs(const char *data)
// {
//     const int bytesPerLED = 3; // R, G, B
//     int ledIndex = 0;
//     int offset = 0;

//     while (offset < NUM_LEDS * bytesPerLED && data[offset] != '\0')
//     {
//         int r = data[offset];
//         int g = data[offset + 1];
//         int b = data[offset + 2];

//         leds[ledIndex] = CRGB(r, g, b);
//         ledIndex++;
//         offset += bytesPerLED;
//     }

//     FastLED.show();
// }