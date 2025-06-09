import cv2
import time
from ultralytics import YOLO
from loguru import logger

# Carrega o modelo treinado
model = YOLO("runs/detect/train2/weights/best.pt")

# Inicializa a webcam (0 = webcam padrão)
cap = cv2.VideoCapture(2)

# Verifica se a câmera foi aberta corretamente
if not cap.isOpened():
    logger.debug("Erro ao abrir a webcam.")
    exit()

logger.debug("Pressione 'q' na janela de vídeo ou CTRL+C no terminal para sair.")

try:
    while True:
        # Aguarda o usuário apertar Enter no terminal
        input("Pressione Enter para capturar um frame...")

        # Captura um frame
        ret, frame = cap.read()
        if not ret:
            logger.debug("Erro ao capturar frame.")
            break

        start = time.time()

        # Roda inferência
        results = model(frame)

        end = time.time()
        logger.debug(f"Inferência concluída em {end - start:.3f} segundos")

        # Desenha e exibe
        annotated = results[0].plot()
        cv2.imshow("Detecção YOLOv8", annotated)

        # Aguarda o usuário ver a imagem
        logger.debug("Visualizando resultado. Feche a janela ou pressione qualquer tecla nela.")
        cv2.waitKey(0)  # trava até interação com a janela

        # Fecha a janela após visualização
        cv2.destroyAllWindows()

        # Espera um pouco antes de continuar (reduz carga no sistema)
        time.sleep(0.5)

except KeyboardInterrupt:
    logger.debug("\nExecução encerrada pelo usuário.")

finally:
    cap.release()
    cv2.destroyAllWindows()
