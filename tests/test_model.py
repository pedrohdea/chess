import cv2 as cv
from loguru import logger


def detectAndDisplay(frame):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    # -- Detect faces
    faces = cat_cascade.detectMultiScale(frame_gray)
    for x, y, w, h in faces:
        logger.debug('face: ',x, y)
        center = (x + w // 2, y + h // 2)
        frame = cv.ellipse(frame, center, (w // 2, h // 2), 0, 0, 360, (255, 0, 255), 4)
        faceROI = frame_gray[y : y + h, x : x + w]
        # -- In each face, detect eyes
        # eyes = eyes_cascade.detectMultiScale(faceROI)
        # for x2, y2, w2, h2 in eyes:
        #     logger.debug('eye: ',x2, y2)
        #     eye_center = (x + x2 + w2 // 2, y + y2 + h2 // 2)
        #     radius = int(round((w2 + h2) * 0.25))
        #     frame = cv.circle(frame, eye_center, radius, (255, 0, 0), 4)
        cv.imshow('Capture - Face detection', frame)

cat_cascade_name = 'cascade/cascade.xml'
cat_cascade = cv.CascadeClassifier()
# -- 1. Load the cascades
if not cat_cascade.load(cv.samples.findFile(cat_cascade_name)):
    logger.debug('--(!)Error loading face cascade')
    exit(0)

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
    if cv.waitKey(10) == 27:
        continue
