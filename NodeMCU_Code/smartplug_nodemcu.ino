#include <FS.h>    
//for to connect to wifi.
#include <ESP8266WiFi.h>
#include <ESP8266WiFiMulti.h>
#include <ESP8266HTTPClient.h>

#include <ESP8266WebServer.h>          
#include <DNSServer.h>
#include <WiFiManager.h>          //https://github.com/tzapu/WiFiManager

#include "EmonLib.h"

#define RELAY_PIN D0
#define HOTSPOT_PIN D4

EnergyMonitor emon1;

WiFiClient upload_http_client;      //sending data to website.

//same server for both getting and setting data.
const char* http_server = "sriki007.pythonanywhere.com";

//for getting values.
HTTPClient http;  
String s_payload;
String o_f_payload;

int count=1;
WiFiManager wifiManager;

int POWERCOUNT=1;
int HOTSPOTCOUNT;
double Power,current;

////HardCode Wifi Credentials
//char* ssid="JARVIS";
//char* password="";

//void wificonnect()
//{
//  WiFi.begin(ssid,password);
//  while(WiFi.status()!=WL_CONNECTED)
//  {
//      Serial.print(".");
//      delay(300);
//  }
//  Serial.println(" ");
//}


void wifi()
{
  
  //exit after config instead of connecting
  wifiManager.setBreakAfterConfig(true);

  //wifiManager.resetSettings();

  //tries to connect to last known settings
  //if it does not connect it starts an access point with the specified name
  //here  "AutoConnectAP" with password "password"
  //and goes into a blocking loop awaiting configuration
  if (!wifiManager.autoConnect("SmartPlug", "password")) {
    Serial.println("failed to connect, we should reset as see if it connects");
    delay(3000);
    ESP.reset();
    delay(5000);
  }

  //if you get here you have connected to the WiFi
  Serial.println("connected...yeey :)");

  Serial.println("local ip");
  Serial.println(WiFi.localIP());
}
void wifireset()
{
//exit after config instead of connecting
  //wifiManager.setBreakAfterConfig(true);

  wifiManager.resetSettings();
  delay(500);
  //tries to connect to last known settings
  //if it does not connect it starts an access point with the specified name
  //here  "AutoConnectAP" with password "password"
  //and goes into a blocking loop awaiting configuration

    ESP.reset();
  

  //if you get here you have connected to the WiFi
  Serial.println("connected...yeey :)");

 // Serial.println("local ip");
//  Serial.println(WiFi.localIP());
  
}


void calculate_power()
{ 
  current = emon1.calcIrms(1480);  // Calculate Irms only
  Power=current*230;
}


void upload_http_connect()
{    
    //for http server.
    if (upload_http_client.connect(http_server,80))
     {        
      upload_http_client.print(String("GET /upload_pc_data?power="+String(Power/100.0)+"&"+"current="+String(current/100.0)) + " HTTP/1.1\r\n" +"Host: " + http_server + "\r\n" + "Connection: close\r\n\r\n");
     Serial.println(Power);
     Serial.println(String(Power));     
     Serial.println(current);
     }
     else
     {
      Serial.println("There was a problem in connecting to server... pls check once.");
     }
     upload_http_client.stop();
     delay(10000);//for data uploading.
} 

String on_off_http_client()
{
   http.begin("http://sriki007.pythonanywhere.com/getonoffvalue");
   int httpCode = http.GET();
   o_f_payload = http.getString();
   http.end();
   Serial.println("at on");
   Serial.println(o_f_payload);
   return o_f_payload;
}

String schecdule_http_client()
{
      http.begin("http://sriki007.pythonanywhere.com/getschedulevalue");
      int httpCode = http.GET();
      s_payload = http.getString();
      http.end();
      Serial.println("at off");
      Serial.println(s_payload);
      return s_payload;
}

void setup() {
  Serial.begin(115200);
  pinMode(RELAY_PIN, OUTPUT);
  emon1.current(A0, 111.1); 
  pinMode(A0, INPUT);
  pinMode(HOTSPOT_PIN,INPUT);
  
  wifi();
}

void loop()
{ 
  bool HOTSPOT=digitalRead(HOTSPOT_PIN);
     if(digitalRead(HOTSPOT_PIN)==LOW)
    {
      Serial.println(digitalRead(HOTSPOT_PIN));
      Serial.println("Hotspot reset");
       wifireset();
    }
     if(strlen(WiFi.localIP().toString().c_str())==0)
    {
      Serial.println("Jarvis reconnect");
      wifi();
    }
        if(on_off_http_client()=="1" && schecdule_http_client()=="1")
      { Serial.println("in upload");
        calculate_power();
        upload_http_connect();
        Serial.println("great");
        Serial.println("upload done");
        digitalWrite(RELAY_PIN,0);
      }
      else
      { Serial.println("in else");
        digitalWrite(RELAY_PIN,1);
  
}
}
