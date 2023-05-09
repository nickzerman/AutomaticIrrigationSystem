#include <WiFi.h>
#include <ThingSpeak.h>
#include <FirebaseESP32.h>
#include "time.h"
#include "addons/TokenHelper.h"
#include "addons/RTDBHelper.h"

#define FIREBASE_HOST "link"
#define FIREBASE_AUTH "key"

#define RX 16
#define TX 17

FirebaseData fData;

const char* ssid = "ssid";
const char* password = "password";

const char* ntpServer = "europe.pool.ntp.org";
const long gmtOffset_sec = 3600;
const int daylightOffset_sec = 3600;

WiFiClient client;

unsigned long thingspeakChannel = number;
const char* APIKey = "apikey";

unsigned long getDataPrevMillis=0;
unsigned long getHourPrevMillis=0;

struct tm timeinfo;

int lightingBK=0;
int umidityBK=0;

char year[3];
char month[3];
char day[3];
char hour[3]="00";
char minutes[3]="00";

void setup() {
  Firebase.begin(FIREBASE_HOST,FIREBASE_AUTH);
  Firebase.reconnectWiFi(true);
  
  Serial.begin(115200);
  Serial1.begin(9600,SERIAL_8N1,RX,TX);

  WiFi.mode(WIFI_STA);
  ThingSpeak.begin(client);

  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
}

void loop() {
  if(WiFi.status() != WL_CONNECTED){
    Serial.print("Connection attempt...");
    while(WiFi.status() != WL_CONNECTED){
      WiFi.begin(ssid,password);
      delay(5000);
    }
    Serial.println("\Connected.");
  }

  String reader;
  if(Serial1.available()){
    reader = Serial1.readString();
  }

  if(reader.equals("D")){
    sendDataArduino();
  } 
  else if(reader.equals("H")){
    sendHoursArduino();
  }
  else {
    char* readerC = (char*) reader.c_str();

    int counter=1;
    char* token;
    token = strtok(readerC,";");
  
    while(token!=NULL){
      ThingSpeak.setField(counter,token);
      token=strtok(NULL,";");
      counter++;
    }
    
    ThingSpeak.writeFields(thingspeakChannel,APIKey);
  }

  if(Firebase.ready() && (millis()-getDataPrevMillis > 5000 || getDataPrevMillis == 0)){
    getDataPrevMillis = millis();
    int umidity;
    int lighting;
    if(Firebase.RTDB.getInt(&fData,"/illuminazione")){
      if(fData.dataType()=="int"){
        lighting = fData.intData();
      }
    }
    if(Firebase.RTDB.getInt(&fData,"/umidita")){
      if(fData.dataType()=="int"){
        umidity = fData.intData();
      }
    }
    if(umidity!=umidityBK || lighting!=lightingBK){
      umidityBK = umidity;
      lightingBK = lighting;
      sendDataArduino();
    }
  }

  if(millis()-getHourPrevMillis > 5000 || getHourPrevMillis==0){
    getHourPrevMillis = millis();

    if(getLocalTime(&timeinfo)){
      strftime(year,3,"%y",&timeinfo);

      strftime(month,3,"%m",&timeinfo);

      strftime(day,3,"%d",&timeinfo);
      
      char timeHour[3];
      strftime(timeHour,3,"%H",&timeinfo);
    
      char timeMinutes[3];
      strftime(timeMinutes,3,"%M",&timeinfo);
  
      if(strcmp(hour,timeHour)!=0 || strcmp(minutes,timeMinutes)!=0){
        strcpy(hour,timeHour);
        strcpy(minutes,timeMinutes);
        sendHoursArduino();
      }
    }
  }
}

void sendDataArduino(){
  Serial1.println((String) "D;" + umidityBK + ";" + lightingBK);
}

void sendHoursArduino(){
  Serial1.print((String) "H;" + day + ";" + month + ";" + year + ";" + hour + ";" + minutes);
}
