# NeuroBand ESP32 Firmware: Signal Acquisition and Wireless Communication

This document provides a detailed explanation of the ESP32 firmware for the NeuroBand project. This firmware is responsible for acquiring biosignals from the BioAmp sensor and transmitting them wirelessly to a desktop application using WebSocket communication.

## 1. Overview

The ESP32 acts as the bridge between the BioAmp sensor and the NeuroBand desktop application. It reads analog data from the BioAmp, converts it into a digital format, and then streams this data over Wi-Fi using WebSockets. This setup ensures real-time, low-latency data transfer, which is crucial for brain-computer interface applications.

## 2. Hardware Requirements

To implement this firmware, you will need the following hardware components:

-   **ESP32 Development Board:** Any standard ESP32 development board (e.g., ESP32 DevKitC, NodeMCU ESP32) will work.
-   **BioAmp Sensor:** Such as the EXG Pill or a similar biosignal amplifier. This sensor will provide the raw EEG/ECG analog data.
-   **Electrodes:** For connecting the BioAmp sensor to the user (e.g., forehead for EEG, chest for ECG).
-   **Jumper Wires:** For connecting the BioAmp to the ESP32.
-   **USB Cable:** For programming the ESP32.

## 3. Software Requirements

Before compiling and uploading the firmware, ensure you have the following software installed:

-   **Arduino IDE:** The integrated development environment for ESP32 programming.
-   **ESP32 Board Package for Arduino IDE:** Install this through the Arduino IDE Boards Manager.
-   **Libraries:**
    -   `WiFi.h`: Standard ESP32 Wi-Fi library (usually pre-installed).
    -   `AsyncTCP.h`: Required for `ESPAsyncWebServer`.
    -   `ESPAsyncWebServer.h`: For creating an asynchronous web server and WebSocket server on the ESP32.

    You can install `AsyncTCP` and `ESPAsyncWebServer` via the Arduino IDE Library Manager (Sketch > Include Library > Manage Libraries...).

## 4. Firmware Code (`NeuroBand_ESP32_Firmware.ino`)

Below is the complete code for the ESP32 firmware, along with explanations for each section.

```cpp
// NeuroBand_ESP32_Firmware.ino

#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Server port for data transmission
const uint16_t serverPort = 8080;
AsyncWebServer server(serverPort);
AsyncWebSocket ws("/ws"); // WebSocket for real-time data

// BioAmp sensor pin (example, adjust based on your BioAmp connection)
const int bioAmpPin = 34; // Assuming analog input pin

void setup() {
  Serial.begin(115200);
  pinMode(bioAmpPin, INPUT);

  // Connect to Wi-Fi
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting...");
  }
  Serial.println("WiFi connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // WebSocket event handlers
  ws.onEvent(onWsEvent);
  server.addHandler(&ws);

  // Start server
  server.begin();
  Serial.println("Web Server started");
}

void loop() {
  // Read analog data from BioAmp
  int analogValue = analogRead(bioAmpPin);

  // Prepare data to send (e.g., JSON format)
  String data = "{\"timestamp\";" + String(millis()) + ",\"eeg\";" + String(analogValue) + "}";

  // Send data to connected WebSocket clients
  ws.textAll(data);

  delay(10); // Adjust delay based on desired sampling rate
}

void onWsEvent(AsyncWebSocket * server, AsyncWebSocketClient * client, AwsEventType type, void * arg, uint8_t *data, size_t len) {
  if(type == WS_EVT_CONNECT){
    Serial.printf("WebSocket client #%u connected from %s\\n", client->id(), client->remoteIP().toString().c_str());
  } else if(type == WS_EVT_DISCONNECT){
    Serial.printf("WebSocket client #%u disconnected\\n", client->id());
  } else if(type == WS_EVT_DATA){
    // Handle incoming data if needed
  }
}
```

## 5. Code Explanation

-   **Includes:** The necessary libraries for Wi-Fi connectivity, asynchronous TCP communication, and the web server are included.
-   **WiFi Credentials:** `ssid` and `password` variables need to be updated with your local Wi-Fi network credentials.
-   **Server Port:** The `serverPort` is set to `8080`, which is where the WebSocket server will listen for connections from the desktop application.
-   **`AsyncWebServer` and `AsyncWebSocket`:** These objects are initialized to handle HTTP requests and WebSocket communication, respectively.
-   **`bioAmpPin`:** This constant defines the analog input pin on the ESP32 where the BioAmp sensor's output will be connected. **You must verify and adjust this pin number based on your specific BioAmp module and how you wire it to the ESP32.** Common analog pins on ESP32 include GPIO32-39.
-   **`setup()` function:**
    -   Initializes serial communication for debugging.
    -   Sets the `bioAmpPin` as an input.
    -   Connects the ESP32 to the specified Wi-Fi network.
    -   Configures WebSocket event handlers (`onWsEvent`) and adds the WebSocket to the web server.
    -   Starts the web server.
-   **`loop()` function:**
    -   Continuously reads the analog value from the `bioAmpPin`.
    -   Constructs a JSON-formatted string containing a timestamp (using `millis()`) and the analog BioAmp reading. This format is easy to parse on the desktop application side.
    -   Sends this JSON data to all connected WebSocket clients using `ws.textAll(data)`.
    -   A `delay(10)` is included to control the sampling rate. This means data is sent approximately every 10 milliseconds (100 Hz). You can adjust this value based on your application's needs; a smaller delay means a higher sampling rate but also higher power consumption and network traffic.
-   **`onWsEvent()` function:** This callback function handles different WebSocket events:
    -   `WS_EVT_CONNECT`: Fired when a new client connects to the WebSocket. It prints the client's ID and IP address to the serial monitor.
    -   `WS_EVT_DISCONNECT`: Fired when a client disconnects.
    -   `WS_EVT_DATA`: This is where you would handle any data sent *from* the desktop application *to* the ESP32, if your project requires two-way communication. Currently, it's empty as the primary flow is ESP32 to desktop.

## 6. How to Use

1.  **Open in Arduino IDE:** Open the `NeuroBand_ESP32_Firmware.ino` file in the Arduino IDE.
2.  **Install Libraries:** Ensure you have installed `AsyncTCP` and `ESPAsyncWebServer` libraries via the Arduino IDE Library Manager.
3.  **Configure Board:** Select your ESP32 board from Tools > Board.
4.  **Update Wi-Fi Credentials:** Change `YOUR_WIFI_SSID` and `YOUR_WIFI_PASSWORD` to your actual Wi-Fi network details.
5.  **Verify BioAmp Pin:** Double-check the `bioAmpPin` constant and ensure it matches the physical connection of your BioAmp sensor to the ESP32.
6.  **Upload Firmware:** Connect your ESP32 board to your computer via USB and upload the firmware.
7.  **Monitor Serial Output:** Open the Serial Monitor in Arduino IDE (Tools > Serial Monitor) to see the Wi-Fi connection status and debug messages.

Once uploaded, your ESP32 will connect to your Wi-Fi network and start streaming BioAmp data via WebSockets. The next step would be to develop the desktop application to receive and process this data.

## 7. Next Steps (Desktop Application)

After successfully deploying this firmware, the next crucial step is to develop the desktop application that will:

-   Connect to the ESP32's WebSocket server.
-   Receive the JSON data stream.
-   Parse the `timestamp` and `eeg` (or `ecg`) values.
-   Perform signal processing (e.g., blink detection, heart rate calculation).
-   Implement the brain-controlled interface and GUI dashboard functionalities.

This firmware provides the foundational data stream for the entire NeuroBand system. Ensure it is stable and reliably transmitting data before moving on to the desktop application development.


