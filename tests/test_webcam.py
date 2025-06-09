from __future__ import print_function
import cv2 as cv
from time import time

from loguru import logger

cat_cascade_name = 'cascade/cascade.xml'
cat_cascade = cv.CascadeClassifier()
# -- 1. Load the cascades
if not cat_cascade.load(cv.samples.findFile(cat_cascade_name)):
    logger.debug('--(!)Error loading face cascade')
    exit(0)


cap = cv.VideoCapture(0)

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
        cv.imwrite('positivas/{}.jpg'.format(loop_time), frame)
        logger.debug('imagem positiva salva')
    elif key == ord('n'):
        cv.imwrite('negativas/{}.jpg'.format(loop_time), frame)
        logger.debug('imagem negativa salva')
