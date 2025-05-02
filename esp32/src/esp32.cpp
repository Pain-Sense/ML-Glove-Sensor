/**
 * @brief This file includes some of the code made by Guilherme Escada, 
 * the predecesor of this project
 * 
 * @author Guilherme Escada
 * @author Christian Fernandes
 */

#include "DFRobot_Heartrate.h"
#include <WiFi.h>
#include <PubSubClient.h> 
#include "sd_read_write.h"
#include "SD_MMC.h"

// Sensor GSR
const int ADC1 = 32; 
int ADC1_VALUE = 0;
float ADC1_AVERAGE = 0;
float ADC1_RESISTANCE = 0;
int DEBUG_GSR = 0;  // Debug
int GSR_CALIBRATION = 0;  // Quando fizeres a calibração não uses o sensor. Abre o serial plotter, ajusta a resistência da placa para minimizar o output e aponta o valor em que ficar
int GSR_CALIBRATION_VALUE = 2000;

// Sensor PPG
const int ADC2 = 33;
int ADC2_VALUE = 0;
int PPG_HEART_RATE = 0;
int DEBUG_PPG = 0; // Debug
int PPG_HEART_RATE_MODE = 0; // Modo Heart Rate; É necessário estar igual no sensor e descomentar a linha abaixo quando on
// DFRobot_Heartrate heartrate(DIGITAL_MODE);
int PPG_ECG_MODE = 1; // Modo ECG; É necessário estar igual no sensor e descomentar a linha abaixo quando on
DFRobot_Heartrate heartrate(ANALOG_MODE); 

// Cartão de memória
int ID = 0;
int C = 0;
int MC = 0;
String FILE_NAME = "";
String FILE_DATA = "";
#define SD_MMC_CMD 15 // Não mudar!
#define SD_MMC_CLK 14 // Não mudar! 
#define SD_MMC_D0  2  // Não mudar!
int DEBUG_MC = 0;

// TODO: We need to change this -----------------
// WiFi
const char* ROUTER_SSID = "Portátil Escada";
const char* ROUTER_PASSWORD = "5J;2r536";
int ATTEMPTS = 0;
int DEBUG_W = 0;

// WiFi Client
WiFiClient WIFI_CLIENT;

// Pub Sub Client (MQTT)
IPAddress PSC_BROKER_IP(192, 168, 137, 1); // IP do broker MQTT (igual ao do pc no hotspot)
const int PSC_BROKER_PORT = 1883; // Porta (MQTT) do broker MQTT
int DEBUG_PSC = 0;
PubSubClient PUB_SUB_CLIENT(WIFI_CLIENT);
// TODO -----------------------------------------


// * Function declarations

/**
 * @brief Receive MQTT message
 * 
 * @param topic topic of the message
 * @param payload content of the message
 * @param length message's size
 */
void receive_MQTT_message(const char* topic, const byte* payload, unsigned int length);

/**
 * @brief Reconnect to MQTT broker
 */
void reconnect_MQTT();


void setup() {
  analogSetAttenuation(ADC_11db);  // Coloca a atenuação em 11db para se medir até 3.9 V em todos os canais de todos os ADCs
  Serial.begin(115200);
  delay(1000); // Para estabilização

  // WiFi
  WiFi.mode(WIFI_STA);
  WiFi.begin(ROUTER_SSID, ROUTER_PASSWORD);
  if (DEBUG_W) {
    Serial.println("Conectando à rede: " + String(ROUTER_SSID));
  }

  while (WiFi.status() != WL_CONNECTED && ATTEMPTS < 20) {
    if (DEBUG_W) {
      Serial.print(".");
    }

    delay(500);
    ATTEMPTS++;
  }

  if (DEBUG_W && WiFi.status() == WL_CONNECTED) {
    Serial.println("Ligado. IP local: " + WiFi.localIP().toString());
  } else if (DEBUG_W && WiFi.status() != WL_CONNECTED) {
    Serial.println("Falha ao ligar ao WiFi. Estado: " + String(WiFi.status()));
  }

  // Cartão de memória
  SD_MMC.setPins(SD_MMC_CLK, SD_MMC_CMD, SD_MMC_D0);
  if (!SD_MMC.begin("/sdcard", true, true, SDMMC_FREQ_DEFAULT, 5)) {
    if (DEBUG_MC) {
      Serial.println("Erro: falha ao montar o cartão.");
    }
    return;
  }

  uint8_t cardType = SD_MMC.cardType();
  if(cardType == CARD_NONE){
    if (DEBUG_MC) {
      Serial.println("Erro: sem cartão.");
    }
    return;
  }

  if (DEBUG_MC){
    Serial.print("Tipo de cartão: ");
  }

  if(cardType == CARD_MMC){
      if (DEBUG_MC) {Serial.println("MMC");}
  } else if(cardType == CARD_SD){
      if (DEBUG_MC) {Serial.println("SDSC");}
  } else if(cardType == CARD_SDHC){
      if (DEBUG_MC) {Serial.println("SDHC");}
  } else {
      if (DEBUG_MC) {Serial.println("Desconhecido");}
  }
  uint64_t cardSize = SD_MMC.cardSize() / (1024 * 1024);
  if (DEBUG_MC) {Serial.printf("Espaço do cartão: %lluMB\n", cardSize);}
  if (DEBUG_MC) {listDir(SD_MMC, "/", 0);}
  if (DEBUG_MC) {
    Serial.printf("Total space: %lluMB\r\n", SD_MMC.totalBytes() / (1024 * 1024));
    Serial.printf("Used space: %lluMB\r\n", SD_MMC.usedBytes() / (1024 * 1024));
  }

  // Pub Sub Client (MQTT)
  PUB_SUB_CLIENT.setServer(PSC_BROKER_IP, PSC_BROKER_PORT); 
  PUB_SUB_CLIENT.setKeepAlive(60);
  PUB_SUB_CLIENT.setCallback(receive_MQTT_message); 
  if (!PUB_SUB_CLIENT.connected()) {
    reconnect_MQTT();
  }
}

void loop() {
  if (GSR_CALIBRATION) {
    ADC1_VALUE = 0;
    for (int i=0;i<10;i++) { // Média de 10 valores para evitar pequenas falhas
      ADC1_VALUE += analogRead(ADC1);
      delay(5);
    }
    ADC1_AVERAGE = ADC1_VALUE / 10;
    Serial.println(ADC1_AVERAGE);
  }
  // VALUE
  ADC1_VALUE = analogRead(ADC1); // ESP32 - 12 bit ADC (0 a 4095);
  // RESISTANCE
  if (ADC1_VALUE < GSR_CALIBRATION_VALUE) {
    ADC1_RESISTANCE = ((4095 + 2 * ADC1_VALUE) * 10000) / (GSR_CALIBRATION_VALUE - ADC1_VALUE); // [Ω]; ESP32 - 12 bit ADC (0 a 4095); // Human Resistance = ((1024 + 2 x Serial_Port_Reading) x 10000)/(Serial_calibration - Serial_Port_Reading) para 10 bit ADC; Serial_calibration é o valor tirado da calibração
  } else {
    if (DEBUG_GSR) {Serial.println("Coloque o sensor GSR");}
  }
  if (DEBUG_GSR) {
    Serial.println("Sensor GSR - Value = " + String(ADC1_VALUE));
    Serial.println("Sensor GSR - Resistance = " + String(ADC1_RESISTANCE));
  }

  // Sensor PPG
  // HEART RATE
  if (PPG_HEART_RATE_MODE) {
    heartrate.getValue(ADC2);
    PPG_HEART_RATE = heartrate.getRate();
    if (DEBUG_PPG)  {
      if (PPG_HEART_RATE) {Serial.println("Sensor PPG - Heart Rate = " + String(PPG_HEART_RATE));}
    }
  }
  // ECG
  if (PPG_ECG_MODE) {
    ADC2_VALUE = analogRead(ADC2);
    if (DEBUG_PPG) {
      Serial.println("Sensor PPG - Heart Value = " + String(ADC2_VALUE));
    }
  }

  // Cartão de memória
  if (MC) {
    FILE_NAME = "/ID" + String(ID) + "C" + String(C) + ".txt";
    if (PPG_HEART_RATE_MODE) {FILE_DATA = "GSR: " + String(ADC1_RESISTANCE) + ", PPG_HR: " + String(PPG_HEART_RATE) + "\n";}
    if (PPG_ECG_MODE) {FILE_DATA = "GSR: " + String(ADC1_RESISTANCE) + ", PPG_V: " + String(ADC2_VALUE) + "\n";}
    // Verifica se o ficheiro já existe e escreve/atualiza os dados
    if (!SD_MMC.exists(FILE_NAME)) {
        writeFile(SD_MMC, FILE_NAME.c_str(), FILE_DATA.c_str());
    } else {
        appendFile(SD_MMC, FILE_NAME.c_str(), FILE_DATA.c_str());
    }
  }

  // Pub Sub Client (MQTT)
  // Manter a ligação
  if (!PUB_SUB_CLIENT.connected()) {
    reconnect_MQTT();
  }
  PUB_SUB_CLIENT.loop(); 
  // Publicar mensagens
  PUB_SUB_CLIENT.publish("GSR", String(ADC1_RESISTANCE).c_str());
  if (PPG_HEART_RATE_MODE) {PUB_SUB_CLIENT.publish("PPG_HR", String(PPG_HEART_RATE).c_str());}
  if (PPG_ECG_MODE) {PUB_SUB_CLIENT.publish("PPG_V", String(ADC2_VALUE).c_str());}

  // Delay
  delay(200);
}

// Function implementations
void receive_MQTT_message(const char* topic, const byte* payload, unsigned int length) {
  String TEMP_MSG = ""; 

  for (int i = 0; i < length; i++) {
    TEMP_MSG += (char) payload[i];
  }

  if (DEBUG_PSC) {
    Serial.println("PubSubClient - Tópico: " + String(topic));
    Serial.println("PubSubClient - Payload: " + String(TEMP_MSG));
  }

  if (strcmp(topic, "ID") == 0) {
    ID = TEMP_MSG.toInt();
    if (DEBUG_PSC) {
      Serial.println("PubSubClient - ID do Paciente: " + String(ID));
    }
  }

  if (strcmp(topic, "C") == 0) {
    C = TEMP_MSG.toInt();
    if (DEBUG_PSC) {
      Serial.println("PubSubClient - Consulta: " + String(C));
    }
  }

  if (strcmp(topic, "MC") == 0) {
    MC = TEMP_MSG.toInt();
    if (DEBUG_PSC) {
      Serial.println("PubSubClient - Log: " + String(MC));
    }
  }
}

void reconnect_MQTT() {
  while (!PUB_SUB_CLIENT.connected()) {
    if (DEBUG_PSC) {
      Serial.print("Tentando conectar ao broker MQTT...");
    }

    if (PUB_SUB_CLIENT.connect("ESP32")) {
      PUB_SUB_CLIENT.subscribe("ID");
      PUB_SUB_CLIENT.subscribe("C");
      PUB_SUB_CLIENT.subscribe("MC");

      if (DEBUG_PSC) {
        Serial.println("Ligado ao broker MQTT e subscrito aos tópicos.");
      }

    } else {
      Serial.print(".");
      delay(500);
    }
  }
}
