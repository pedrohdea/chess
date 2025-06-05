#define LED_STATUS 13

#define DATA_PIN   8 //SER
#define CLOCK_PIN  9 //SRCLK
#define LATCH_PIN 10 //RCLK

void setup() {  
  pinMode(LED_STATUS, OUTPUT);
  pinMode(DATA_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
  pinMode(LATCH_PIN, OUTPUT);
  
  digitalWrite(LED_STATUS, HIGH); // Liga LED
  
  Serial.begin(9600);
  Serial.println("Arduino pronto");
}

void loop() {
  if (Serial.available() >= 2) {
    uint8_t linha = Serial.read();  // LINHA LSB (coils 0–7)
    uint8_t coluna = Serial.read(); // COLUNA MSB (coils 8–15)
    digitalWrite(LED_STATUS, HIGH); // Liga LED
 
    // Print binário dos dois bytes
    Serial.print("Recebido -> linha: ");
    Serial.print(linha, BIN);
    Serial.print(" | coluna: ");
    Serial.println(coluna, BIN);
    delay(1000);
    digitalWrite(LED_STATUS, LOW); // Liga LED

    uint8_t leds[2];
    leds[0] = linha;
    leds[1] = coluna;

    escreverShiftRegister(leds);  // Atualiza os registradores
  }
}

void escreverShiftRegister(uint8_t leds[2]) {
  digitalWrite(LATCH_PIN, LOW);
  shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, leds[1]); // byte mais significativo
  shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, leds[0]); // byte menos significativo
  digitalWrite(LATCH_PIN, HIGH);
}