#include <ArduinoHttpClient.h>
#include <ArduinoJson.h>
#include <WiFiNINA.h>

char ssid[] = "SoteloNetwork";
char password[] = "1turr1aga";

int status = WL_IDLE_STATUS;

char server[] = "564b-2806-107e-13-9f5c-d12f-83fd-bae-f0c0.ngrok.io";    //Always modify when re-run ngrok

WiFiClient client;

void setup(){
  Serial.begin(9600);

  while (status != WL_CONNECTED) {
    Serial.println("Attempting to connect to Network: ");
    Serial.println(ssid);
    status = WiFi.begin(ssid,password);
    delay (1000);
  }

  Serial.print("Connected to SSID: ");
  Serial.println(WiFi.SSID());
  IPAddress ip = WiFi.localIP();
  IPAddress gateway = WiFi.gatewayIP();
  Serial.print("IP Address: ");
  Serial.println(ip);

}

void loop(){

  DynamicJsonDocument doc1(1024);
  
  float adc_MQ = analogRead(A0);
  float voltaje = adc_MQ * (5.0 /1023.0);
  float rs = 1000*( (5-voltaje) / voltaje);
  double co2 = .4091*pow(rs/5463, -1.497); // Regresion de co2: 105.68x + 219.8R²
  
  doc1["valor"] = co2;
  doc1["idParametro"] = 1;
  doc1["idDispositivo"] = 1;

  String postData1;

  serializeJson(doc1, postData1);

   if (client.connect(server, 80)) {
    client.println("POST /mediciones/agregar HTTP/1.1");
    client.println("Host: 564b-2806-107e-13-9f5c-d12f-83fd-bae-f0c0.ngrok.io");
    client.println("Content-Type: application/json");
    client.print("Content-Length: ");
    client.println(postData1.length());
    client.println();
    client.print(postData1);
   }

  if (client.connected()) {
    client.stop();
  }
  
  Serial.println(postData1);

  delay(500);
  
}
