import time

import cv2  # OpenCV para carregar e manipular imagens
from loguru import logger
from engine.detect import get_yolo_detect, get_pecas_colors
from engine.predict import get_pecas


IMAGE_PATH = "positivas/1749519069.4164693.jpg"  # Make sure this path is correct
img = cv2.imread(IMAGE_PATH)

# Marca o tempo de início da inferência
# Realiza a inferência na imagem
start = time.time()
logger.debug("Início:", time.strftime("%H:%M:%S", time.localtime(start)))

detections, annotated_display_frame = get_yolo_detect(img)
# Marca o tempo de fim da inferência
end = time.time()
logger.debug("Fim:", time.strftime("%H:%M:%S", time.localtime(end)))
logger.debug(f"Duração: {end - start:.3f} segundos")

#################
start = time.time()
logger.debug("Início:", time.strftime("%H:%M:%S", time.localtime(start)))

pecas = get_pecas(detections, 32)
get_pecas_colors(pecas, img)
# Marca o tempo de fim da inferência
end = time.time()
logger.debug("Fim:", time.strftime("%H:%M:%S", time.localtime(end)))
logger.debug(f"Duração: {end - start:.3f} segundos")


cv2.imshow("YOLO Single Image Detection", annotated_display_frame)
cv2.waitKey(0)  # Wait indefinitely until a key is pressed

input('\nsair?')
cv2.destroyAllWindows()
logger.info("Script finished.")
