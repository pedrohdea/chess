import sys
from engine.predict import get_matrix, get_command
from engine.send_move import send_move
from engine.predict import get_pecas, get_matrix, get_mapa
import cv2 as cv
from time import time, sleep
import numpy as np
from stockfish import Stockfish
from loguru import logger
import serial

LOG_LEVEL = "INFO"

logger.remove()
logger.add(
    sys.stdout,
    level=LOG_LEVEL,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <level>{message}</level>",
)

# Adiciona o logger para arquivo rotativo de 5MB
logger.add(
    "logs/log_{time:YYYY-MM-DD}.log",
    rotation="5 MB",
    retention=5,
    compression="zip",
    level=LOG_LEVEL,
    format="{time} {level} {message}",
)

# SETUP
ENDERECO_USB = "/dev/ttyACM0"
ARDUINO = serial.Serial(port=ENDERECO_USB, baudrate=9600, timeout=1)

MAPA = None
STOCKFISH = Stockfish(path="stockfish/stockfish-ubuntu-x86-64")
start_matrix = np.array(
    [
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1],
    ]
)
last_frame = None
numero_de_jogadas = 0
pecas_restantes = 32
cap = cv.VideoCapture(2)
# liga todos os leds, apresentação

while not numero_de_jogadas:
    sleep(1)
    ret, frame = cap.read()
    cv.imshow("Tabuleiro de Xadrez", frame)
    if cv.waitKey(30) & 0xFF == ord("q"):
        raise KeyboardInterrupt()

    pecas = get_pecas(frame, 32)
    if len(pecas) < 32:
        logger.info("Procurando 32 peças pra inicialização...")
        continue
    elif not MAPA:
        MAPA = get_mapa(pecas)
        frame_matrix = get_matrix(pecas, MAPA)
        if np.array_equal(start_matrix, frame_matrix):
            logger.info("INICIALIZADO COM SUCESSO")
            last_frame = frame_matrix
            break
        else:
            MAPA = None
            logger.info("Esperando organizar 32 peças...")


# LOOP
try:
    while True:
        loop_time = time()

        ret, frame = cap.read()
        if not ret:
            logger.info("--(!) No captured frame -- Break!")
            raise ValueError("Troque a opção de entrada de vídeo")

        cv.imshow("Tabuleiro de Xadrez", frame)
        if cv.waitKey(30) & 0xFF == ord("q"):
            raise KeyboardInterrupt()

        pecas = get_pecas(frame, pecas_restantes)
        frame_matrix = get_matrix(pecas, MAPA)
        if frame_matrix is None:
            logger.warning("Frame perdido")
            continue
        modify_frame = last_frame - frame_matrix
        count_pos = np.count_nonzero(modify_frame == 1)
        count_neg = np.count_nonzero(modify_frame == -1)

        if count_pos == 1 and count_neg == 1:
            command = get_command(modify_frame)
            trust_command = command
            if command != trust_command:
                sleep(1)
                continue

            try:
                STOCKFISH.make_moves_from_current_position([command])  # Player ou Bot
            except ValueError as stck_exc:
                logger.warning(f"STOCKFISH: {stck_exc}")
                sleep(1)
                continue

            logger.success(STOCKFISH.get_board_visual())
            logger.success(f'comando reconhecido {command}')
            # send_move(ARDUINO, command)
            sleep(1)
            numero_de_jogadas += 1
            last_frame = frame_matrix
            move = STOCKFISH.get_best_move()
            send_move(ARDUINO, move)
            logger.info(f"Realizando jogada {move}")
        else:
            logger.debug("Nenhum movimento detectado...")

finally:
    cap.release()
    cv.destroyAllWindows()
    logger.info("\n[INFO] Encerrado com sucesso.")
