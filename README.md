![Arduino](https://img.shields.io/badge/-Arduino-00979D?style=for-the-badge&logo=Arduino&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
![Firebase](https://img.shields.io/badge/firebase-%23039BE5.svg?style=for-the-badge&logo=firebase)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white)

## Introduzione

Il progetto ha lo scopo di gestire l'irrigazione di una pianta in modo automatico, evitando la disidratazione del terreno. <br />
Per questo, sono state utilizzate due schede comunicanti: un **Arduino UNO** e un **ESP32 Thing Plus**. <br /><br />
L'**Arduino** è responsabile di determinare se la pianta ha bisogno di essere irrigata, utilizzando vari sensori. Grazie ad opportuni controlli, non si irriga eccessivamente la pianta, evitando di danneggiarla. <br />
Attraverso un sensore di livello dell’acqua viene monitorata la quantità di acqua disponibile. Nel caso in cui il livello dell’acqua fosse basso, viene segnalato il problema mediante l’accensione di un LED. <br />
Un display OLED 128x64, collegato all'Arduino, mostra l'ora e la data corrente (ricevuti dall'ESP32), la temperatura e l'umidità ambientale. <br />
Infine, ogni 16 secondi, l'Arduino invia i valori dei vari sensori all'ESP32, che saranno memorizzati in cloud (ThingSpeak).<br /><br />
L'**ESP32** ha il compito di inviare i dati all'Arduino (ora/data e soglie delle threshold) quando richiesto e quando necessario, oltre a memorizzare i valori dei vari sensori nel cloud per la visualizzazione tramite un'interfaccia web.<br /><br />
Infatti, è stata realizzata un'interfaccia web, utilizzando Dash e Plotly, con lo scopo di:
  - recuperare i dati dal cloud e mostrarli attraverso opportuni grafici;
  - permettere l'aggiornamento delle soglie di umidità e illuminazione.

<img src="images/schema.jpg" width="700">

## Componenti Utilizzati

- Arudino Uno
- ESP32 Thing Plus
- Display OLED
- x3 LED
- x3 Resistenze (330 ohm)
- Sensore di Luminosità
- Sensore di Temperatura e Umidità Ambientale
- Sensore di Umidità del Terreno
- Sensore di Livello dell'Acqua
- Sensore di Movimento
- Relay
- Pompetta (con alimentatore)

## Librerie utilizzate

- **TimerOne**: per la gestione del timer dell'Arduino
- **u8g**: per la gestione del display OLED
- **SofwareSerial**: per poter connettere l’esp32 a internet
- **Wifi**: per permettere la connessione dell'ESP ad internet
- **Cactus_io_SHT15**: per poter permette la lettura del sensore di temperatura e umidità ambientale
- **ThingSpeak**: per permettere all'ESP la scrittura dei dati su ThingSpeak
- **FirebaseESP32**: per permette all'ESP la lettura dei dati presenti sul Realtime Database di Firebase

## Schema Collegamenti

<img src="images/fritzing.png" width="700">

## Bibliografia

Per la creazione dell'interfaccia web, e per la risoluzione dei vari problemi affrontati ci siamo affidati a:
  - https://dash.plotly.com/

Per l'utilizzo e il funzionamento della libreria u8g abbiamo utilizzato la documentazione presente su github: 
  - https://github.com/olikraus/u8glib/wiki/userreference

Per l'utilizzo dei vari sensori abbiamo trovato utili le seguenti guide:
  - https://randomnerdtutorials.com/guide-for-oled-display-with-arduino/
  - https://lastminuteengineers.com/water-level-sensor-arduino-tutorial/
  - https://lastminuteengineers.com/soil-moisture-sensor-arduino-tutorial/
  - https://arduinogetstarted.com/tutorials/arduino-relay
  - https://randomnerdtutorials.com/arduino-with-pir-motion-sensor/

Per la soluzione ad eventuali problemi, sia hardware che software, ci siamo appoggiati ai vari forum riguardanti Arduino.
