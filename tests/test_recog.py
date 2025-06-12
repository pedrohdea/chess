import cv2
import time
import os
from loguru import logger
from engine.detect import get_yolo_detect


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

        detections, annotated_display_frame = get_yolo_detect(frame)

        # === EXIBIÇÃO ===
        cv2.imshow("YOLO ONNX Webcam", annotated_display_frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    logger.debug("\n[INFO] Encerrado com sucesso.")
