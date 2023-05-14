#include <SoftwareSerial.h>
#include <TimerOne.h>
#include <U8glib.h>
#include <cactus_io_SHT15.h>

//Definition Digital PIN
#define PIRMotion 3 //Pin used for PIR Motion Sensor
#define redLED 7 //Pin used for the Red LED
#define yellowLED 6 //Pin used for the Yellow LED
#define greenLED 5 //Pin used for the Green LED
#define relay 2 //Pin used for the Relay
#define SHT_Data 10 //Pin used for the 'Data' output of the Temperature and Humidity Sensor
#define SHT_Clock 11 //Pin used for the 'Clock' output of the Temperature and Humidity Sensor

//Deffinition Analogic PIN
#define soilMoisture A3 //Pin user for the Soil Moisture Sensor
#define lightSensor A0 //Pin used for the light sensor
#define waterSensor A2 //Pin user for the Water Level Sensor

//Serial port used for the communication with ESP32
SoftwareSerial espSerial(12,13); // RX, TX

//Definition of the Temperature and Humidity Sensor
SHT15 sht = SHT15(SHT_Data,SHT_Clock); 

//Definition of the display (monitor)
U8GLIB_SH1106_128X64 u8g(U8G_I2C_OPT_NONE); //Analogic: A4 and A5

bool checkInterrupt = false; //When it's true Arduino sends all the informations to the ESP32, otherwise Arduino does nothing
bool checkUmidity = true;

//Variable used for all the checks and for the display
int umidityThreshold;
int lightingThreshold;

char year[3];
char month[3];
char day[3];
char hours[3];
char minutes[3];

String hour;
String date;

void setup() {
  pinMode(redLED,OUTPUT);
  pinMode(yellowLED,OUTPUT);
  pinMode(greenLED,OUTPUT);
  pinMode(PIRMotion,INPUT_PULLUP);
  pinMode(relay,OUTPUT);

  pinMode(soilMoisture,INPUT);
  pinMode(lightSensor,INPUT);
  pinMode(waterSensor,INPUT);

  digitalWrite(redLED,HIGH);
  digitalWrite(yellowLED,HIGH);
  digitalWrite(greenLED,HIGH);

  delay(5000);

  Serial.begin(9600);
  espSerial.begin(9600);
  
  espSerial.print("Handshake"); //D --> Request Data
  while(!espSerial.available()){}

  u8g.setFont(u8g_font_unifont);
  showDisplay();

  Timer1.initialize(8000000);
  Timer1.attachInterrupt(sendDataESP);
  attachInterrupt(digitalPinToInterrupt(PIRMotion),showDisplay,CHANGE);
}

void loop() { 
  while(espSerial.available()){
    String reader = "";
    char c;
    while(espSerial.available()){
      c = espSerial.read();
      if(c=='\n'){
        break;
      } else {
        reader = reader + c;
      }
    }
    if(reader[0]=='D'){
      receiveDataESP(reader);
    }
    else if(reader[0]=='H'){
      receiveHoursESP(reader);
    }
  }

  if(analogRead(waterSensor)<50){ //50 by default
    digitalWrite(redLED,HIGH);
  } else {
    digitalWrite(redLED,LOW);
  }

  Serial.println((String) "Soglia Umidità: " + umidityThreshold);
  if(analogRead(soilMoisture)<umidityThreshold){
    digitalWrite(greenLED,HIGH);
    digitalWrite(yellowLED,LOW);
    digitalWrite(relay, HIGH);
    delay(800);
    digitalWrite(relay, LOW);
    delay(5000);
  } else {
    digitalWrite(yellowLED,HIGH);
    digitalWrite(greenLED,LOW);
  }
  delay(1000);
}

void receiveDataESP(String reader){
  char* readerC = (char*) reader.c_str();

  char* token;
  token = strtok(readerC,";");
  token=strtok(NULL,";"); //Avoid first token

  while(token!=NULL){
    //Serial.println((String) "Hum"+ token);
    if(checkUmidity){
      umidityThreshold = atoi(token); //String to int
      checkUmidity=!checkUmidity;
    }
    else{
      lightingThreshold = atoi(token); //String to int
      checkUmidity=!checkUmidity;
    }
    token=strtok(NULL,";"); //Next token
  }
}

void receiveHoursESP(String reader){
  char* readerC = (char*) reader.c_str();

  char* token;
  token = strtok(readerC,";");
  token = strtok(NULL,";"); //Avoid first token

  int counter = 1;
  while(token!=NULL){
    switch(counter){
      case 1:
        date = token;
        break;
      case 2:
        hour = token;
    }
    counter++;
    token=strtok(NULL,";"); //Next token
  }
}

void showDisplay(){
  sht.readSensor();
  
  char tempStr[5];
  float temp = sht.getTemperature_C();
  dtostrf(temp, 2, 1, tempStr);
  String tempF = (String)tempStr + " " + "°C";

  char umidStr[5];
  float umid = sht.getHumidity();
  dtostrf(umid, 2, 1, umidStr);
  String umidF = (String)umidStr + " %";
  
  if(digitalRead(PIRMotion)==HIGH){
    u8g.firstPage();
    do {
      u8g.setFont(u8g_font_7x13r);
      u8g.setFontPosBaseline();
      u8g.setPrintPos(20,27);
      u8g.print(hour);

      u8g.setFont(u8g_font_6x10r);
      u8g.setFontPosTop();
      u8g.setPrintPos(14,37);
      u8g.print(date);

      u8g.setFont(u8g_font_6x13r);
      u8g.setFontPosBaseline();
      u8g.setPrintPos(84,29);
      u8g.print(tempF);

      u8g.setFontPosTop();
      u8g.setPrintPos(84,35);
      u8g.print(umidF);

      u8g.drawFrame(0,0,128,64);
      u8g.drawLine(10,32,65,32);
      u8g.drawLine(75,7,75,57);

      u8g.setContrast(200);
    } while (u8g.nextPage());
  } else {
    u8g.firstPage();
    do {
    } while (u8g.nextPage());
  }
}

void sendDataESP(){
  if(checkInterrupt){
    sht.readSensor();
    espSerial.println((String)analogRead(soilMoisture) + ";" + sht.getHumidity() + ";" + sht.getTemperature_C() + ";" + analogRead(lightSensor));
    checkInterrupt=!checkInterrupt;
  } else {
    checkInterrupt=!checkInterrupt;
  }
}
