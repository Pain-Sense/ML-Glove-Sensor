#include <Wire.h>
#include "RTClib.h"
#include "DFRobot_Heartrate.h"
#include <WiFi.h>
#include <WiFiManager.h>
#include <PubSubClient.h> 

RTC_DS3231 rtc;
const int gsrPin = 32; // Pin connected to the GSR sensor
int gsrValue = 0;

const int ppgPin = 34; // Pin connected to the PPG sensor
int ppgValue = 0;
DFRobot_Heartrate heartrate(DIGITAL_MODE);
int PPG_HEART_RATE = 0;

const int numReadings = 10; // Number of readings to average

WiFiClient espClient;
PubSubClient client(espClient);

const char* mqtt_server = "192.168.1.66"; 


void setupWiFi() {
  WiFiManager wm;
  // wm.resetSettings(); // Uncomment this if you want to reset saved WiFi credentials
  if (!wm.autoConnect("TestAP", "password")) {
    Serial.println("Failed to connect");
    ESP.restart();
  }
  Serial.println("Connected! IP:");
  Serial.println(WiFi.localIP());
}

void connectMQTT() {
  client.setServer(mqtt_server, 1883);
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
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


void setup () {
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
  setupWiFi(); 
  connectMQTT();

}




void loop () {

 // Read and average GSR sensor values
  for (int i = 0; i < numReadings; i++) {
    gsrValue += analogRead(gsrPin);
    delay(10); 
  }


  // Read and average PPG sensor values
  for (int i = 0; i < numReadings; i++) {
    ppgValue += analogRead(ppgPin);
    delay(10);
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
  heartrate.getValue(ppgPin);
  PPG_HEART_RATE = heartrate.getRate();
  Serial.print("PPG 2 Value: "); // não percebo como é que isto é suposto funcionar
  Serial.println(PPG_HEART_RATE);
  delay(100);

// MQTT publishing
  if (!client.connected()) {
    connectMQTT();
  }
  client.loop();



                     String payload = String("{\"timestamp\":\"") +
                   String(now.timestamp()) + "\",\"bvp\":" +
                   ppgValue + ",\"gsr\":" +
                   gsrValue + ",\"id\":" +
                   10 + "}";


  client.publish("sensors", payload.c_str());
  Serial.println("Published to MQTT: " + payload);

  delay(1000);

}