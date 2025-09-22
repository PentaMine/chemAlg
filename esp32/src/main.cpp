#include <Arduino.h>

uint32_t t;
uint16_t v; 

void setup() {
  pinMode(35, INPUT);
  Serial.begin(115200);
}

void loop() {
  t = micros();
  v = analogRead(35);
  
  Serial.write((int)((t >> 24) & 0xFF) );
  Serial.write((int)((t >> 16) & 0xFF) );
  Serial.write((int)((t >> 8) & 0xFF) );
  Serial.write((int)((t >> 0) & 0xFF) );

  Serial.write((int)((v >> 8) & 0xFF) );
  Serial.write((int)((v >> 0) & 0xFF) );

  Serial.write("\xb3\x8f\x0f\xf8");
}
