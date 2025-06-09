from pi74HC595 import pi74HC595
import RPi.GPIO as gpio
import multiprocessing, time
from loguru import logger


def liga_tabuleiro(tabuleiro_1: list, tabuleiro_2: list):
    # gpio.setmode(gpio.BOARD)
    # shift_register = pi74HC595(daisy_chain=2)

    while True:
        # Ajustar time para 0.015
        time.sleep(1)
        # shift_register.set_by_list(tabuleiro_1)
        logger.debug(f'1: {tabuleiro_1}')
        time.sleep(1)
        # shift_register.set_by_list(tabuleiro_2)
        logger.debug(f'2: {tabuleiro_2}')

    # shift_register.get_values()
    ##[0, 0, 0, 0, 0, 0, 0, 0]


eixo_x = [False, False, False, False, False, False, False, False]
eixo_y = [True, True, True, True, True, True, True, True]


def get_vetor_led(posicao_xadrez):
    # posicao_xadrez='a8a6'
    x1, y1 = posicao_xadrez[0], posicao_xadrez[1]
    x2, y2 = posicao_xadrez[2], posicao_xadrez[3]

    alfabeto = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    x1 = alfabeto.index(x1)
    y1 = int(y1)
    x2 = alfabeto.index(x2)
    y2 = int(y2)

    novo_eixo_x = eixo_x
    novo_eixo_y = eixo_y

    novo_eixo_x[x1] = not eixo_x[x1]
    novo_eixo_y[y2] = not eixo_y[x2]
    tabuleiro_1 = novo_eixo_x + novo_eixo_y

    novo_eixo_x = eixo_x
    novo_eixo_y = eixo_y

    novo_eixo_x[x2] = not eixo_x[x2]
    novo_eixo_y[y2] = not eixo_y[x2]
    tabuleiro_2 = novo_eixo_x + novo_eixo_y
    return tabuleiro_1, tabuleiro_2


tabuleiro_1, tabuleiro_2 = get_vetor_led('a8a6')


proc = multiprocessing.Process(
    target=liga_tabuleiro, args=(tabuleiro_1, tabuleiro_2)
)
proc.start()
logger.debug(proc)
# Terminate the process
t = 20
while t:
    t -=1
    time.sleep(0.5)
    logger.debug('AAAAAAAAAAAAAAAAA')

proc.terminate()  # sends a SIGTERM
