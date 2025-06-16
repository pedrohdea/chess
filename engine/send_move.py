from time import sleep

from loguru import logger


def send_move(arduino, move: str):
    move = move.upper().strip()
    logger.debug(f"enviando comando {move}.")
    try:
        arduino.write(f"{move}\n".encode())
    except:
        logger.warning(f"comando {move} não enviado")
        arduino.close()
        sleep(1)
        arduino.open()
