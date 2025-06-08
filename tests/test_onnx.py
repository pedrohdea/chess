import cv2
import onnxruntime as ort
import numpy as np
import time

# Caminho do modelo
onnx_model_path = "runs/detect/train2/weights/best.onnx"
session = ort.InferenceSession(onnx_model_path)
input_name = session.get_inputs()[0].name

# Carrega imagem e redimensiona
img = cv2.imread('positivas/1749319728.0928051.jpg')
img = cv2.resize(img, (640, 640))  # ajuste para o input do modelo

# Pré-processamento
img_input = img[:, :, ::-1]            # BGR → RGB
img_input = img_input.transpose(2, 0, 1) / 255.0  # CHW + normalização
img_input = np.expand_dims(img_input, axis=0).astype(np.float32)

# Inferência e tempo
start = time.time()
outputs = session.run(None, {input_name: img_input})
end = time.time()

# Pós-processamento básico
pred = outputs[0][0]
conf_thres = 0.25
num_detected = sum(1 for det in pred if det[4] > conf_thres)

# Saída
print(f"Inferência concluída em {end - start:.3f} segundos")
print(f"Objetos detectados com confiança > {conf_thres}: {num_detected}")
