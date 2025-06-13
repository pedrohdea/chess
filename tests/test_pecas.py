import cv2
import time
from engine.predict import get_pecas, get_matrix, get_mapa
from loguru import logger

# === INICIALIZA WEBCAM ===
logger.debug("[INFO] Iniciando webcam...")
cap = cv2.VideoCapture(0)
time.sleep(2)

if not cap.isOpened():
    raise RuntimeError("Erro ao abrir a webcam.")

logger.debug("Pressione 'q' para sair.\n")
MAPA = None

try:
    while True:
        time.sleep(1)
        ret, frame = cap.read()
        if not ret:
            logger.debug("[ERRO] Frame não capturado.")
            break

        # === EXIBIÇÃO ===
        cv2.imshow("Linhas do Tabuleiro", frame)
        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

        pecas = get_pecas(frame, 32)
        if len(pecas) < 32:
            continue

        if not MAPA:
            MAPA = get_mapa(pecas)

        frame_matrix = get_matrix(pecas, MAPA)

        logger.debug(frame_matrix)


finally:
    cap.release()
    cv2.destroyAllWindows()
    logger.debug("\n[INFO] Encerrado com sucesso.")
