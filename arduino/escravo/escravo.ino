
#define LED_STATUS 13
#define BAUDRATE 9600

#define NUM_COILS 16  // total real de saídas do seu hardware

#define DATA_PIN   8 //SER
#define CLOCK_PIN  9 //SRCLK
#define LATCH_PIN 10 //RCLK

byte endereco_escravo = 1;

void loop() {
  if (Serial.available()) {
    char comando = Serial.read();

    if (comando == 'L') {
      digitalWrite(LED_STATUS, HIGH); // Liga LED
    } else if (comando == 'D') {
      digitalWrite(LED_STATUS, LOW); // Desliga LED
    }
  }
}

// Envia os 2 bytes para os 74HC595 (coils 0-15)
void escreverShiftRegister(uint8_t leds[2]) {
  digitalWrite(LATCH_PIN, LOW);
  shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, leds[1]); // byte mais significativo
  shiftOut(DATA_PIN, CLOCK_PIN, MSBFIRST, leds[0]); // byte menos significativo
  digitalWrite(LATCH_PIN, HIGH);
}

void blink(int sec) {
  uint8_t leds[2] = {0b11111111, 0b00000000}; // Liga coils 0–7
  escreverShiftRegister(leds); // liga tudo
  delay(sec);

  leds[0] = 0b00000000;
  leds[1] = 0b11111111; // Liga coils 8–15
  escreverShiftRegister(leds); // desliga tudo
}

void setup() {
  Serial.begin(BAUDRATE); // Inicia a comunicação serial
  pinMode(LED_STATUS, OUTPUT); // LED onboard
  digitalWrite(LED_STATUS, HIGH); // Liga LED

  Serial.println("V0.4");

  pinMode(LED_STATUS, OUTPUT);
  pinMode(RS485_ENABLE, OUTPUT);
  digitalWrite(RS485_ENABLE, LOW);  // começa recebendo

  pinMode(DATA_PIN, OUTPUT);
  pinMode(CLOCK_PIN, OUTPUT);
  pinMode(LATCH_PIN, OUTPUT);

  blink(1000);

  Serial.print("Endereço Modbus configurado: ");
  Serial.println(endereco_escravo);
}

void debugPrintFrame(const byte *frame, int length, const char *label = "Enviando") {
  Serial.print("📤 ");
  Serial.print(label);
  Serial.print(" [");
  for (int i = 0; i < length; i++) {
    if (i > 0) Serial.print(" ");
    if (frame[i] < 0x10) Serial.print("0");
    Serial.print(frame[i], HEX);
  }
  Serial.println("]");
}

void enviaFrame(const byte *dados, int tamanho, const char *label = "Resposta") {
  if (dados[0] != 0) {  // não responde a broadcast
    digitalWrite(RS485_ENABLE, HIGH);
    Serial.write(dados, tamanho);
    Serial.flush();
    digitalWrite(RS485_ENABLE, LOW);
    delay(10);
    debugPrintFrame(dados, tamanho, label);  // imprime no monitor
  }
}

void enviaExcecao(byte *req, byte codigo) {
  byte resp[5];
  resp[0] = req[0];              // ID do escravo
  resp[1] = req[1] | 0x80;       // Função com MSB ativado (ex: 0x8F)
  resp[2] = codigo;              // Código da exceção

  uint16_t crcVal = crc.Modbus(resp, 0, 3);
  resp[3] = crcVal & 0xFF;
  resp[4] = (uint8_t)(crcVal >> 8);

  enviaFrame(resp, 5, "exceção");
}

void funcaoWriteMultipleCoils(byte *receivedData) {
  uint16_t addr = (receivedData[2] << 8) | receivedData[3];
  uint16_t quantity = (receivedData[4] << 8) | receivedData[5];
  byte byteCount = receivedData[6];
  int tamEsperado = 7 + byteCount + 2;  // header + dados + CRC

  // Validação de endereço de registrador (coils)
  if (addr >= NUM_COILS || (addr + quantity) > NUM_COILS) {
    enviaExcecao(receivedData, 0x02);  // registrador inválido
    return;
  }

  // Validação de dado: byteCount precisa bater com a quantidade de coils
  if (byteCount != (quantity + 7) / 8) {
    enviaExcecao(receivedData, 0x03);  // dado inválido
    return;
  }
  blink(50);

  // Aplica valores aos coils reais conforme os bits em receivedData[7..]
  // Copia os dados recebidos para o shift register
  uint8_t dados[2] = {0};
  for (int i = 0; i < byteCount && i < 2; i++) {
    dados[i] = receivedData[7 + i];
  }
  dados[1] = ~dados[1];

  // Monta resposta conforme especificação Modbus (eco parcial da requisição)
  byte resp[8];
  resp[0] = receivedData[0];  // ID escravo
  resp[1] = 0x0F;             // função
  resp[2] = receivedData[2];  // Addr High
  resp[3] = receivedData[3];  // Addr Low
  resp[4] = receivedData[4];  // Qtd High
  resp[5] = receivedData[5];  // Qtd Low

  uint16_t crcResp = crc.Modbus(resp, 0, 6);
  resp[6] = crcResp & 0xFF;
  resp[7] = (uint8_t)(crcResp >> 8);

  enviaFrame(resp, 8, "resposta write multiple coils");
}


void funcaoInvalida(byte *receivedData) {
  // Resposta de exceção: função inválida (exception code 0x01)
  byte respEx[5];
  respEx[0] = receivedData[0];        // ID escravo
  respEx[1] = receivedData[1] | 0x80; // função com MSB ativado (ex: 0x8F)
  respEx[2] = 0x01;                   // código de exceção: função inválida

  uint16_t crcEx = crc.Modbus(respEx, 0, 3);
  respEx[3] = crcEx & 0xFF;           // CRC LSB
  respEx[4] = (crcEx >> 8) & 0xFF;    // CRC MSB

  enviaFrame(respEx, 5, "função inválida");
}

void loop() {
  if (Serial.available()) {
    char comando = Serial.read();

    if (comando == 'L') {
  byte receivedData[64];
  int bytesAvailable;
  long milisegundos;

  // Aguarda início de recepção
  if (Serial.available() > 0) {
    bytesAvailable = Serial.available();
    milisegundos = millis();

    bool endFrame = false;
    while (!endFrame) {
      if (Serial.available() != bytesAvailable) {
        bytesAvailable = Serial.available();
        milisegundos = millis();
      } else {
        if ((millis() - milisegundos) > END_FRAME_TIME) {
          endFrame = true;
        }
      }
    }

    // Lê os bytes disponíveis
    int tam = Serial.available();
    Serial.readBytes(receivedData, tam);

    // Valida o CRC
    valueCrc = crc.Modbus(receivedData, 0, tam);

    if (valueCrc == 0) {
      // Indica sucesso no LED
      digitalWrite(LED_STATUS, HIGH);
      delay(50);
      digitalWrite(LED_STATUS, LOW);

      // verifica se o endereço é para este escravo
      if (receivedData[0] == endereco_escravo || receivedData[0] == 0) {
        if (receivedData[1] == 0x0F) {
          escreverShiftRegister(dados);
        } else if (receivedData[1] == 0x0E) {
          enviaFrame(receivedData, tam, "função eco");
        } else {
          funcaoInvalida(receivedData);
        }
      }
    } else {
      // CRC inválido, ignora
    }
  }
}
