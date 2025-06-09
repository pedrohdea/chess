import cv2                     # OpenCV para carregar e manipular imagens
from ultralytics import YOLO  # Biblioteca Ultralytics com modelo YOLOv8
import time                   # Para medir o tempo de execução
from loguru import logger

# Carrega o modelo YOLO treinado (substitua pelo caminho correto do seu modelo)
model = YOLO("runs/detect/train2/weights/best.pt")

# Marca o tempo de início da inferência
start = time.time()
logger.debug('Início:', time.strftime('%H:%M:%S', time.localtime(start)))

# Carrega a imagem de teste
img = cv2.imread('positivas/1749319728.0928051.jpg')

# Realiza a inferência na imagem
results = model(img)

# Marca o tempo de fim da inferência
end = time.time()
logger.debug('Fim:', time.strftime('%H:%M:%S', time.localtime(end)))
logger.debug(f'Duração: {end - start:.3f} segundos')

# Exibe a imagem com as detecções em uma janela (usa backend interno da Ultralytics)
results[0].show()
