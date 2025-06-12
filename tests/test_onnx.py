import time

import cv2
import numpy as np
import onnxruntime as ort
from loguru import logger

from engine.draw import draw_squares, letterbox

# === CONFIGURAÇÕES ===
MODEL_PATH = "runs/detect/train3/weights/best.onnx"
IMAGE_PATH = "positivas/1749519069.4164693.jpg"
INPUT_SIZE = 640

session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

frame = cv2.imread(IMAGE_PATH)
if frame is None:
    logger.error(f"Erro ao carregar a imagem: {IMAGE_PATH}")
    exit()

img, ratio, dwdh = letterbox(frame, (INPUT_SIZE, INPUT_SIZE))
img_input = img.astype(np.float32) / 255.0
img_input = np.transpose(img_input, (2, 0, 1))
img_input = np.expand_dims(img_input, axis=0)

logger.debug(f"[DEBUG] Shape da entrada: {img_input.shape}")

# === INFERÊNCIA ===
start = time.time()
output = session.run([output_name], {input_name: img_input})[0]
end = time.time()

logger.debug(f"Shape da saída: {output.shape}")
logger.debug(f"Tempo de inferência: {end - start:.3f} s")
pred = output[0]  # (num_dets, 6) # Assuming output[0] contains the detections

frame = draw_squares(frame, pred, ratio, dwdh)
cv2.imshow("DEBUG squares", frame)

# Add these lines to make the window persistent and close properly
if cv2.waitKey(30) & 0xFF == ord("q"):
    raise KeyboardInterrupt()

input("\nsair?")
cv2.destroyAllWindows()
