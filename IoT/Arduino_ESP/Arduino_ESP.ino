/*
 * author: Nguyễn Thành Chung
 * date: 14/10/2021
*/

#include <DHT.h>
//#include <ArduinoJson.h>

#include <ESP8266WiFi.h>
#include <PubSubClient.h>


#define DHTTYPE DHT11 // DHT 11
const int DHTPin = 5;

//#define led1 D3
#define led 15 // D8
#define fan 4 // D2
#define rain 13 // D7
#define soil 12 // D6

DHT sensor(DHTPin, DHTTYPE);


const char* ssid = "Chung";
const char* password = "123456789";


const char* mqtt_server = "broker.hivemq.com";
const char* mqtt_username = "NguyenChung";
const char* mqtt_password = "chung0609";

WiFiClient mangcb;
PubSubClient client(mangcb);

unsigned long interval = 5000;
unsigned long previousMillis = 0;


void setup_wifi() {

  delay(100);
  
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // loop toi khi ket noi toi mqtt
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    
    String clientId = "mangcb-";
    clientId += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void callback(char* topic, byte* payload, unsigned int length) 
{
  //-----------------------------------------------------------------

  Serial.print("Co tin nhan moi tu topic: ");
  Serial.println(topic);
  char p[length + 1];
  memcpy(p, payload, length);
  p[length] = NULL;
  String message(p);
  
 if(String (topic) == "device"){
    if (message == "led on") {
    digitalWrite(led, HIGH);
    } 
    else if(message == "led off"){
      digitalWrite(led, LOW);
    }
    if (message == "fan on") {
    digitalWrite(fan, HIGH);
    } 
    else if(message == "fan off"){
      digitalWrite(fan, LOW);
    }
  }
  
  Serial.println(message);
  //Serial.write(payload, length);
  Serial.println();
  //-------------------------------------------------------------------------
}

void setup() {
  pinMode(led, OUTPUT);     
  pinMode(fan, OUTPUT);
  pinMode(rain, INPUT);
  pinMode(soil, INPUT);
  
  Serial.begin(9600);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);

  reconnect();

  client.subscribe("device");

  sensor.begin();
  
}


int value = NULL;
void loop() {
 
 int humidity = sensor.readHumidity();
 int temperature = sensor.readTemperature();
 char device[10][10] = {"", "led on", "led off", "fan on", "fan off"};
 while(Serial.available()){
    value = Serial.read();
  }
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
  
  if ((unsigned long)(millis() - previousMillis) >= interval) {
    previousMillis = millis();
    
  //................DHT11.........................  
    char tempString[8];
    sprintf(tempString, "%d",temperature);
    Serial.print("  Temperature: ");
    Serial.print(tempString);
    client.publish("home/Chung/temp", tempString);
    
    char humString[8];
    sprintf(humString, "%d", humidity);
    Serial.print("  Humidity: ");
    Serial.println(humString);
    client.publish("home/Chung/hum", humString);
    
  //................. Rain sensor..................
  
    int value_rain = digitalRead(rain);//Đọc tín hiệu cảm biến mưa
    if (value_rain == HIGH) { // Cảm biến đang không mưa
      Serial.println("sunny");
      client.publish("home/Chung/rain", "sunny");
    } else {
      client.publish("home/Chung/rain", "raining");
      Serial.println("raining");
    }
  //................soil sensor.....................
    int value_soil = analogRead(soil);//Đọc tín hiệu cảm biến mưa
    char soilString[8];
    sprintf(soilString, "%d", value_soil);
    Serial.println(soilString);
    client.publish("home/Chung/soil", soilString);
        
  //................ device contror.................
    if(value == '1'){
      digitalWrite(led,HIGH);
      client.publish("home/Chung/device", device[1]);
      value = NULL;
    }
    else if(value == '0'){
      digitalWrite(led,LOW);
      client.publish("home/Chung/device", device[2]);
      value = NULL;
    }
    else if(value == '3'){
      digitalWrite(fan,HIGH);
      client.publish("home/Chung/device", device[3]);
      value = NULL;
      }
    else if(value == '2'){
      digitalWrite(fan,LOW);
      client.publish("home/Chung/device", device[4]);
      value = NULL;
      }
    else {
      client.publish("home/Chung/device",device[0]);
      }
    }
    
    client.loop();
  

}
