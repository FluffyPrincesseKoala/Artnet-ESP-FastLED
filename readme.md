Here's your **GitHub README in Markdown format**:

```md
# 🌟 ESP-Artnet-LEDs
🚀 **Real-time Art-Net to ESP8266 LED control** using WiFi & FastLED.  
🎨 **Seamlessly integrates with Resolume & other DMX software.**  

---

## 📖 Overview
This project allows you to control **multiple ESP8266-powered LED strips** using **Art-Net over WiFi**, making it easy to sync visuals with music and live performances.

- 🔗 Supports **Resolume, QLC+, MadMapper, and other DMX software**.  
- ⚡ Designed for **low-latency, real-time lighting control**.  
- 🛠 **Test & debug tools included** for easier setup.  

---

## 🚀 Features
✅ **Multi-ESP support** – Add as many ESPs as needed.  
✅ **Buffered Art-Net processing** – Reduces flickering by waiting for all universes.  
✅ **FastLED integration** – Works with WS2812B, SK6812, and more.  
✅ **Real-time Debugging** – CLI visualization for received data.  
✅ **Serial Communication Mode** – Send LED data over USB for local testing.  

---

## 🛠 Installation & Setup
### 1️⃣ Flash the ESP8266
1. Install **Arduino IDE** & add ESP8266 board support.
2. Clone this repo:  
   ```bash
   git clone https://github.com/YOUR_USERNAME/ESP-Artnet-LEDs.git
   cd ESP-Artnet-LEDs
   ```
3. Open `firmware/esp8266_led_controller.ino` in **Arduino IDE**.
4. Edit `config.h` and update:
   ```cpp
   const char* ssid = "YourWiFi"; 
   const char* password = "YourPassword";
   ```
5. Flash to your **ESP8266**.

---

### 2️⃣ Run the Art-Net Listener (Python)
Make sure you have **Python 3** installed.

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the Art-Net listener:
   ```bash
   python python/artnet_listener.py
   ```
3. The terminal should display connected ESPs & incoming data.

---

### 3️⃣ Resolume Art-Net Configuration
#### 🎛 Steps to connect Resolume:
1. **Go to Preferences → DMX**.
2. Enable **Art-Net Output** on **subnet 0, universe 0**.
3. Add a **DMX fixture** with `RGB pixel mapping`.
4. Assign **ESP8266’s IP** to match Resolume’s output.
5. Play a **DMX clip**, and LEDs should respond!

---

## 🎨 Packet Structure (How Data is Sent)
Each **ESP receives data as UDP packets** formatted as:
```
[Art-Net Header][Universe ID][RGB Data]
```
Each ESP **handles full universes** (512 channels, 170 LEDs max per universe).  
If an ESP controls **250 LEDs**, it gets **2 universes**.

---

## 🧪 Testing & Debugging
### 1️⃣ Serial LED Test
Use this for **offline LED control** via USB.
```bash
python serial/sendRainbow.py
```
- Sends a **rainbow effect** to ESP via Serial.

### 2️⃣ Art-Net Debug Mode
```bash
python python/test_send.py
```
- Sends **fake Art-Net data** to simulate Resolume.

### 3️⃣ Real-time CLI Status
The Python script has a **refreshing CLI** that shows:
```
Universe 0: Received ✅  (Sent to 192.168.1.92)
Universe 1: Waiting... ⏳
```

---

## 🔧 Troubleshooting
**1️⃣ LEDs not lighting up?**  
✅ Check ESP8266's **WiFi connection** (`Serial Monitor`).  
✅ Ensure Resolume is **sending Art-Net** (use `test_send.py`).  
✅ Verify **ESP's IP** matches Art-Net config.  

**2️⃣ Flickering LEDs?**  
✅ Ensure **full universe data** is received before sending (`Buffered mode`).  
✅ Use **high-quality power supply** for LEDs.  
✅ Reduce WiFi interference (`2.4GHz congestion`).  

**3️⃣ ESP keeps restarting?**  
✅ Reduce packet size (`config.h`).  
✅ Use a **dedicated power supply** for ESP, not USB.  

---

## 💡 Future Improvements
📌 Support for **ESP32**.  
📌 Add **MQTT & OSC** support for more control.  
📌 Web UI for **live LED preview**.  

---

## 📜 License
MIT License – Use, modify & contribute freely!  

---

## ⭐ Contribute
- **Fork the repo** & submit PRs!
- Open **Issues** if you find bugs!