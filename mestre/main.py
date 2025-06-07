import serial
import time

# Substitua pela sua porta correta (ex: 'COM3' no Windows ou '/dev/ttyUSB0' no Linux)
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)
time.sleep(2)  # Aguarda o Arduino reiniciar após abrir a porta


# Enviar comando # Liga o LED
leds = [0b11111111, 0b00000000]  # [LINHA, COLUNA]
arduino.write(bytearray(leds))

time.sleep(1)

while (1) :

    # Enviar comando # Desliga o LED
    leds = [0b00000010, 0b11111101]  # [LINHA, COLUNA] = 7G
    arduino.write(bytearray(leds))

    # Enviar comando # Desliga o LED
    leds = [0b00000100, 0b11111101]  # [LINHA, COLUNA] = 7G
    arduino.write(bytearray(leds))


arduino.close()