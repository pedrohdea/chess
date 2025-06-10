"""Teste de webcam, usado para coletar imagem da webcam"""

import os
import cv2 as cv
from time import time

from loguru import logger

cap = cv.VideoCapture(2)

if not cap.isOpened:
    logger.debug('--(!)Error opening video capture')
    exit(0)

while True:
    ret, frame = cap.read()
    if frame is None:
        logger.debug('--(!) No captured frame -- Break!')
        continue
    cv.imshow('Capture - Face detection', frame)
    # detectAndDisplay(frame)
    loop_time = time()
    key = cv.waitKey(1)
    if key == ord('q'):
        cv.destroyAllWindows()
        break
    elif key == ord('p'):
        os.makedirs('positivas', exist_ok=True)
        cv.imwrite('positivas/{}.jpg'.format(loop_time), frame)
        logger.debug('imagem positiva salva')
    elif key == ord('n'):
        os.makedirs('negativas', exist_ok=True)
        cv.imwrite('negativas/{}.jpg'.format(loop_time), frame)
        logger.debug('imagem negativa salva')
