from engine.predict import get_predict, get_matrix, get_command, get_area
from engine.send_move import send_move
import cv2 as cv
from time import time
import numpy as np
from stockfish import Stockfish
import logging

stockfish = Stockfish(path='stockfish/stockfish-ubuntu-x86-64')
start_matrix = np.matrix(
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

cap = cv.VideoCapture(0)
while True:
    numero_de_jogadas = 0
    # liga todos os leds, apresentação

    ret, frame = cap.read()
    if frame is None:
        print('--(!) No captured frame -- Break!')
        raise ValueError('Troque a opção de entrada de vídeo')

    cv.imshow('Capturando...', frame)
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    elif key == ord('p'):
        print('detectando imagem')
    else:
        continue

    loop_time = time()

    pecas = get_predict(frame)
    if not pecas:
        continue

    if numero_de_jogadas == 0:
        if len(pecas != 32):
            logging.error('Não encontrado 32 peças')
            continue

        last_frame = start_matrix
        area = get_area(pecas)
        quadrado = area[2] / 8, area[3] / 8

    frame_matrix = get_matrix(pecas, quadrado)
    modify_frame = last_frame - frame_matrix
    command = get_command(modify_frame)

    try:
        stockfish.make_moves_from_current_position([command])  # bot
    except ValueError:
        continue

    print(stockfish.get_board_visual())
    numero_de_jogadas += 1
    last_frame = frame_matrix
    move = stockfish.get_best_move()
    send_move(move)
    print(f'Realizando jogada {move}')
