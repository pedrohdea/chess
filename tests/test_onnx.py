import onnxruntime as ort
import numpy as np
import cv2
import time

# === CONFIGURAÇÕES ===
MODEL_PATH = "runs/detect/train2/weights/best.onnx"
IMAGE_PATH = "positivas/1749319728.0928051.jpg"
INPUT_SIZE = 640  # tamanho esperado pela rede (ex: 640x640)

# === FUNÇÕES AUXILIARES ===


def letterbox(im, new_shape=(640, 640), color=(114, 114, 114)):
    """Redimensiona mantendo a proporção e adiciona padding (como o Ultralytics faz)"""
    shape = im.shape[:2]  # atual: [altura, largura]
    ratio = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    new_unpad = (int(round(shape[1] * ratio)), int(round(shape[0] * ratio)))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]
    dw /= 2
    dh /= 2
    im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(
        im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color
    )
    return im, ratio, (dw, dh)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


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
for det in pred:
    *xyxy, conf, cls = det
    if conf < 0.1:
        continue
    print(det)

    x1, y1, x2, y2 = map(
        int,
        [
            (xyxy[0] - dwdh[0]) / ratio,
            (xyxy[1] - dwdh[1]) / ratio,
            (xyxy[2] - dwdh[0]) / ratio,
            (xyxy[3] - dwdh[1]) / ratio,
        ],
    )

    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    cv2.putText(
        img,
        f"{int(cls)} {conf:.2f}",
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1,
    )

# === EXIBIÇÃO ===
cv2.imshow("Resultado ONNX", img)
key = cv2.waitKey(0)
cv2.destroyAllWindows()
