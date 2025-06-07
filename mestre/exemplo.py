import serial
import time

# Substitua pela sua porta correta (ex: 'COM3' no Windows ou '/dev/ttyUSB0' no Linux)
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=1)
# Aguarda o Arduino reiniciar após abrir a porta
time.sleep(2)

arduino.write('E2E4\n'.encode())
time.sleep(2)
arduino.write('E4E5\n'.encode())

arduino.close()