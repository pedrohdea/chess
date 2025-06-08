import onnxruntime as ort
import numpy as np
import cv2
import time
from engine.draw import *

# === CONFIGURAÇÕES ===
MODEL_PATH = "runs/detect/train2/weights/best.onnx"
IMAGE_PATH = "positivas/1749319728.0928051.jpg"
INPUT_SIZE = 640  # tamanho esperado pela rede (ex: 640x640)

# === INICIALIZAÇÃO DO MODELO ===
session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])

input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name

# === CARREGAR IMAGEM ===
img = cv2.imread(IMAGE_PATH)
img_resized, ratio, dwdh = letterbox(img, (INPUT_SIZE, INPUT_SIZE))
img_input = img_resized.astype(np.float32)
img_input = img_input / 255.0
img_input = np.transpose(img_input, (2, 0, 1))  # HWC → CHW
img_input = np.expand_dims(img_input, axis=0)  # 1xCxHxW

# === INFERÊNCIA ===
start = time.time()
output = session.run([output_name], {input_name: img_input})[0]
end = time.time()

print(f"Inferência em {end - start:.3f} segundos")

# === PÓS-PROCESSAMENTO SIMPLES (só exibição dos boxes) ===
# Supondo saída formato YOLOv8: (1, num_dets, 6) → [x1, y1, x2, y2, conf, cls]
pred = output[0]  # (num_dets, 6)
img = draw_squares(pred, img, ratio, dwdh)

# === EXIBIÇÃO ===
import os
os.environ["QT_QPA_PLATFORM"] = "xcb"  # evita conflitos no Linux

import cv2

cv2.imshow("Resultado ONNX", img)
key = cv2.waitKey(0)
cv2.destroyAllWindows()
