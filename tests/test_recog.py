import cv2
import time
import os
from engine.draw import draw_squares
from engine.predict import get_predict
from loguru import logger

# === EXIBIÇÃO ===
os.environ["QT_QPA_PLATFORM"] = "xcb"  # evita conflitos no Linux

# === INICIALIZA WEBCAM ===
logger.debug("[INFO] Iniciando webcam...")
cap = cv2.VideoCapture(2)
time.sleep(2)

if not cap.isOpened():
    raise RuntimeError("Erro ao abrir a webcam.")

logger.debug("Pressione 'q' para sair.\n")

try:
    while True:
        time.sleep(1)
        ret, frame = cap.read()
        if not ret:
            logger.debug("[ERRO] Frame não capturado.")
            break

        pred, ratio, dwdh = get_predict(frame)

        # === PÓS-PROCESSAMENTO ===
        frame = draw_squares(frame, pred, ratio, dwdh)

        # === EXIBIÇÃO ===
        cv2.imshow("YOLO ONNX Webcam", frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    logger.debug("\n[INFO] Encerrado com sucesso.")
