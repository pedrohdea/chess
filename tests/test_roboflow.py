from roboflow import Roboflow
import cv2 as cv
from PIL import Image
from loguru import logger


rf = Roboflow(api_key="Yc9P3iOmEuSts3mFZLd3")
PROJECT = rf.workspace().project("chess-4jvm8")
MODEL = PROJECT.version(1).model


def get_positions(file_path) -> list:
    # infer on a local image
    prediction = MODEL.predict(file_path, confidence=40, overlap=30).json()
    for pred in prediction['predictions']:
        logger.debug(pred)
        yield pred['x'], pred['y'], pred['width'], pred['height']


def detectAndDisplay(frame):
    im = Image.fromarray(frame)
    im.save("tmp_image.jpg")
    # -- Detect faces
    pecas = get_positions("tmp_image.jpg")
    for x, y, w, h in pecas:
        logger.debug('peça: ', x, y)
        center = (int(x+ (w / 2)), int(y + (h / 2)))
        from IPython import embed;embed(header='C')
        cv.circle(frame, center, 30, (255, 0, 0), 4)
        cv.imshow('Capture - Xadrez detection', frame)


camera_device = 0
# -- 2. Read the video stream
cap = cv.VideoCapture(camera_device)

if not cap.isOpened:
    logger.debug('--(!)Error opening video capture')
    exit(0)

while True:
    ret, frame = cap.read()
    if frame is None:
        logger.debug('--(!) No captured frame -- Break!')
        continue
    detectAndDisplay(frame)
