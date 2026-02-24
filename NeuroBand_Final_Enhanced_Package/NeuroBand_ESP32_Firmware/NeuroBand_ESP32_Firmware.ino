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
    Serial.printf("WebSocket client #%u connected from %s\n", client->id(), client->remoteIP().toString().c_str());
  } else if(type == WS_EVT_DISCONNECT){
    Serial.printf("WebSocket client #%u disconnected\n", client->id());
  } else if(type == WS_EVT_DATA){
    // Handle incoming data if needed
  }
}


