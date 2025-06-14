# Echo server program
import socket
from engine.turn_on_leds import turn_on_leds
from loguru import logger

HOST = "localhost"  # Symbolic name meaning all available interfaces
PORT = 50007  # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        logger.info("Connected by", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                continue
            else:
                turn_on_leds(data.decode())
            conn.sendall(data)
