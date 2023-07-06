// Coded by Pietro Squilla
// Il presente sketch monitora il rumore elettromagnetico e lo sfrutta per generare byte casuali
#include "Arduino_LED_Matrix.h"

// per estrarre il rumore
const int OPAMP_OUT_PIN = A0;
const int SOGLIA_RUMORE = 300;  // valore da 0 a 1023
int counter = 0;
int noiseValue = 0;

// per plot sulla matrice di led
ArduinoLEDMatrix matrix;
int i, j = 0;
bool stop = false;
uint8_t frame[8][12] = {
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0},
  {0,0,0,0,0,0,0,0,0,0,0,0}
};

void setup(){
  Serial.begin(9600);
  matrix.begin();
  
  // risoluzione dell'opamp a 10 bit (valori da 0 a 1023)
  analogReadResolution(10);
}

// funzione per leggere il rumore elettronico
int generateNoise(){
  return analogRead(OPAMP_OUT_PIN);
}

void loop(){
  noiseValue = generateNoise();
  //Serial.println((String)"noise: " + noiseValue); // print di debug per calibrare la soglia
  
  // incrementa la variabile aleatoria
  counter++;
  if(counter > 255){
    counter = 0;
  }
  
  // se il rumore supera la soglia leggi la variabile
  if(noiseValue > SOGLIA_RUMORE){
    Serial.println(counter);
    
    // controllo matrice di led per monitorare senza seriale
    if(!stop){
      frame[i][j] = 1;
      matrix.renderBitmap(frame, 8, 12);
      // conta i numeri trovati sulla matrice di led
      i++;
      if(i >= 8){
        j++;
        i = 0;
      }
    }
    
    // se sono finiti i led non aggiornare più la matrice
    if(j >= 12){
      stop = true;
    }
    
    delay(1000);
  }
  
  //delay(100);
}
