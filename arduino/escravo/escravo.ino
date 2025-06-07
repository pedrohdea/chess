#define LED_STATUS 13

#define DATA_PIN   8 //SER
#define CLOCK_PIN  9 //SRCLK
#define LATCH_PIN 10 //RCLK

#define BAUDRATE   9600

uint8_t ledsDe[2];
uint8_t ledsPara[2];

void escreverShiftRegister(uint8_t leds[2]) {
  digitalWrite(LATCH_PIN, LOW);
  shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, leds[1]);  // MSB (coluna)
  shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, leds[0]);  // LSB (linha)
  digitalWrite(LATCH_PIN, HIGH);
}

void limparComandos() {
  uint8_t limpar[2] = {0b00000000, 0b11111111};
  escreverShiftRegister(limpar);
  ledsDe[0] = limpar[0];
  ledsDe[1] = limpar[1];
  ledsPara[0] = limpar[0];
  ledsPara[1] = limpar[1];
}

uint8_t inverterBits(uint8_t b) {
  uint8_t invertido = 0;
  for (int i = 0; i < 8; i++) {
    invertido <<= 1;
    invertido |= (b & 1);
    b >>= 1;
  }
  return invertido;
}

void gerarMapaUnitario(const char *comando, uint8_t leds[2]) {
  if (!comando || strlen(comando) != 2) {
    leds[0] = 0;
    leds[1] = 0;
    return;
  }

  char col = toupper(comando[0]);
  char lin = comando[1];

  uint8_t coluna = 0;
  uint8_t linha  = 0;

  if (col >= 'A' && col <= 'H')
    coluna = (1 << (col - 'A'));

  if (lin >= '1' && lin <= '8')
    linha = (1 << (lin - '1'));
    linha = inverterBits(linha);

  coluna = ~coluna & 0xFF;  // inversão da coluna

  leds[0] = linha;   // LSB
  leds[1] = coluna;  // MSB
}

void readSerial() {
  digitalWrite(LED_STATUS, HIGH); // Aguardando mensagem

  if (Serial.available() > 0) {
    digitalWrite(LED_STATUS, LOW); // Mensagem recebida

    String comando = Serial.readStringUntil('\n');
    comando.trim();

    if (comando.length() == 4) {
      limparComandos();

      String parte1 = comando.substring(0, 2);  // ex: A3
      String parte2 = comando.substring(2, 4);  // ex: B8

      gerarMapaUnitario(parte1.c_str(), ledsDe);
      gerarMapaUnitario(parte2.c_str(), ledsPara);
    }
  }
}

void setup() {
  pinMode(DATA_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
  pinMode(LATCH_PIN, OUTPUT);
  pinMode(LED_STATUS, OUTPUT); // LED onboard

  digitalWrite(LED_STATUS, HIGH);

  Serial.begin(BAUDRATE);
  Serial.println("V1.0");
  limparComandos();
  delay(500);
}

void loop() {
  readSerial();
  escreverShiftRegister(ledsDe);
  escreverShiftRegister(ledsPara);
}
