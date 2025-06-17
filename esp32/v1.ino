#include <Wire.h>
#include "RTClib.h"
// #include "DFRobot_Heartrate.h"
#include <WiFi.h>
#include "esp_timer.h" 
#include <WiFiManager.h>
#include <PubSubClient.h>
#ifdef ESP32
#include <EEPROM.h>
#endif

RTC_DS3231 rtc;
const int gsrPin = 32; // Pin connected to the GSR sensor
int gsrValue = 0;

const int ppgPin = 34; // Pin connected to the PPG sensor
int ppgValue = 0;
//DFRobot_Heartrate heartrate(DIGITAL_MODE);
//int PPG_HEART_RATE = 0;

const int numReadings = 10; // Number of readings to average

WiFiClient espClient;
PubSubClient client(espClient);

// Define the MQTT server
#define MQTT_SERVER "your_mqtt_broker_ip" // Replace with MQTT broker IP or hostname
char mqtt_server[40] = MQTT_SERVER;      

// Define the default device ID
#define DEFAULT_DEVICE_ID 10
int deviceId = DEFAULT_DEVICE_ID;

#ifdef ESP32
#define EEPROM_SIZE 512
#define MQTT_SERVER_ADDR 0
#define DEVICE_ID_ADDR 40 

void saveMQTTServer(const char* server) {
  EEPROM.begin(EEPROM_SIZE);
  strncpy((char*)EEPROM.getDataPtr(), server, sizeof(mqtt_server));
  EEPROM.commit();
  EEPROM.end();
  Serial.println("MQTT server saved to EEPROM.");
}

void loadMQTTServer() {
  EEPROM.begin(EEPROM_SIZE);
  strncpy(mqtt_server, (const char*)EEPROM.getDataPtr(), sizeof(mqtt_server));
  EEPROM.end();
  Serial.print("MQTT server loaded from EEPROM: ");
  Serial.println(mqtt_server);
}

void saveDeviceId(int id) {
  EEPROM.begin(EEPROM_SIZE);
  EEPROM.put(DEVICE_ID_ADDR, id);
  EEPROM.commit();
  EEPROM.end();
  Serial.println("Device ID saved to EEPROM.");
}

int loadDeviceId() {
  EEPROM.begin(EEPROM_SIZE);
  int loadedId; 
  EEPROM.get(DEVICE_ID_ADDR, loadedId);
  EEPROM.end();
  Serial.print("Device ID loaded from EEPROM: ");
  Serial.println(loadedId);
  return loadedId;
}
#endif

void setupWiFi() {
  WiFiManager wm;
  //wm.resetSettings();  Only reset for debugging purposes.

  //Mqtt can be changes in AP
  WiFiManagerParameter custom_mqtt_server("server", "MQTT Server", mqtt_server, 40);
  wm.addParameter(&custom_mqtt_server);

  //ID can be changes in AP
  String deviceIdStr = String(deviceId);
  WiFiManagerParameter custom_device_id("deviceid", "Device ID", deviceIdStr.c_str(), 10);
  wm.addParameter(&custom_device_id);

  if (!wm.autoConnect("TestAP", "password")) {
    Serial.println("Failed to connect to WiFi");
    ESP.restart();
  }
  Serial.println("Connected to WiFi! IP:");
  Serial.println(WiFi.localIP());

  // After connecting, check if the user entered an MQTT server
  String entered_mqtt_server = custom_mqtt_server.getValue();
  if (entered_mqtt_server.length() > 0) {
    strncpy(mqtt_server, entered_mqtt_server.c_str(), sizeof(mqtt_server));
    mqtt_server[sizeof(mqtt_server) - 1] = '\0'; 
    Serial.print("MQTT Server set by user: ");
    Serial.println(mqtt_server);
    #ifdef ESP32
    saveMQTTServer(mqtt_server); 
    #endif
  } else {
    Serial.print("Using default MQTT Server: ");
    Serial.println(mqtt_server);
    #ifdef ESP32
    if (strlen(mqtt_server) == 0) {
      loadMQTTServer();
    }
    #endif
  }


  String entered_device_id = custom_device_id.getValue();
  if (entered_device_id.length() > 0) {
    deviceId = entered_device_id.toInt();
    Serial.print("Device ID set by user: ");
    Serial.println(deviceId);
    #ifdef ESP32
    saveDeviceId(deviceId); 
    #endif
  } else {
    Serial.print("Using default Device ID: ");
    Serial.println(deviceId);
    #ifdef ESP32
    // If no user input for Device ID, load from EEPROM
    deviceId = loadDeviceId();
    #endif
  }
}

void connectMQTT() {
  client.setServer(mqtt_server, 1883);
  while (!client.connected()) {
    Serial.print("Connecting to MQTT: ");
    Serial.print(mqtt_server);
    Serial.print(" ...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22); // SDA, SCL -> RTC pins

  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }

  if (rtc.lostPower()) {
    Serial.println("RTC lost power, setting time!");
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__))); // Set to compile time
  }

#ifdef ESP32
  loadMQTTServer(); // Load MQTT server from EEPROM if available
  deviceId = loadDeviceId(); // Load Device ID from EEPROM
#endif

  setupWiFi();
  connectMQTT();
}

void loop() {
  // Read and average GSR sensor values
  gsrValue = 0;
  for (int i = 0; i < numReadings; i++) {
    gsrValue += analogRead(gsrPin);
  
  }

  // Read and average PPG sensor values
  ppgValue = 0;
  for (int i = 0; i < numReadings; i++) {
    ppgValue += analogRead(ppgPin);
    
  }

  DateTime now = rtc.now();

  Serial.printf("[%04d-%02d-%02d %02d:%02d:%02d]\n",
                now.year(), now.month(), now.day(),
                now.hour(), now.minute(), now.second());
  gsrValue /= numReadings;
  Serial.print("GSR Value: ");
  Serial.println(gsrValue);
  ppgValue /= numReadings;
  Serial.print("PPG Value: ");
  Serial.println(ppgValue);
  //heartrate.getValue(ppgPin);
  //PPG_HEART_RATE = heartrate.getRate();
  //Serial.print("PPG Heart Rate: ");
  //Serial.println(PPG_HEART_RATE);


  // MQTT publishing
  if (!client.connected()) {
    connectMQTT();
  }
  client.loop();

// Get milliseconds part of the current second
unsigned long ms = millis() % 1000;

// Format timestamp with 6-digit microsecond precision (milliseconds * 1000)



// Get microseconds since boot
uint64_t usec = esp_timer_get_time();
uint32_t microseconds = usec % 1000000;

// Format timestamp with 6-digit microseconds
char timestampBuffer[40];
snprintf(timestampBuffer, sizeof(timestampBuffer),
         "%04d-%02d-%02dT%02d:%02d:%02d.%06luZ",
         now.year(), now.month(), now.day(),
         now.hour(), now.minute(), now.second(),
         microseconds);

String payload = String("{\"timestamp\":\"") +
               String(timestampBuffer) + "\",\"bvp\":" +
               ppgValue + ",\"gsr\":" +
               gsrValue  + ",\"deviceId\":" +
               deviceId + "}";


  client.publish("sensors", payload.c_str());
  Serial.println("Published to MQTT: " + payload);
  // For BVP
String bvpPayload = String("{\"deviceId\":") + deviceId +
                    ",\"timestamp\":\"" + String(timestampBuffer) +
                    "\",\"value\":" + ppgValue + "}";
client.publish(("sensors/bvp"), bvpPayload.c_str());
Serial.println("Published to sensors/bvp: " + bvpPayload);

// For GSR
String gsrPayload = String("{\"deviceId\":") + deviceId +
                    ",\"timestamp\":\"" + String(timestampBuffer) +
                    "\",\"value\":" + gsrValue + "}";
client.publish(("sensors/gsr"), gsrPayload.c_str());
Serial.println("Published to sensors/gsr: " + gsrPayload);

delay(10);
}