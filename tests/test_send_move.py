from engine.send_move import send_move
import serial
import time

ENDERECO_USB = "/dev/ttyACM0"

ARDUINO = serial.Serial(port=ENDERECO_USB, baudrate=9600, timeout=1)


POSITIONS = [f"{col}{row}" for col in "ABCDEFGH" for row in range(1, 9)]
for p, pos in enumerate(POSITIONS):
    if p == 0:
        continue
    comand = f"{POSITIONS[p-1]}{pos}"
    send_move(ARDUINO, comand)
    time.sleep(1)
