import logging
import numpy as np
import onnxruntime as ort
from cv2.typing import MatLike
from engine.model import Peca
from engine.draw import letterbox
from cv2 import UMat
import time


# Cria a sessão ONNX com OpenVINO
# === CONFIGURAÇÕES ===
INPUT_SIZE = 640
MODEL_PATH = "runs/detect/train2/weights/best.onnx"
SESSION = ort.InferenceSession(
    MODEL_PATH, providers=["OpenVINOExecutionProvider", "CPUExecutionProvider"]
)

input_name = SESSION.get_inputs()[0].name
output_name = SESSION.get_outputs()[0].name


def get_predict(frame: UMat):
    img, ratio, dwdh = letterbox(frame, (INPUT_SIZE, INPUT_SIZE))
    img_input = img.astype(np.float32) / 255.0
    img_input = np.transpose(img_input, (2, 0, 1))  # HWC → CHW
    img_input = np.expand_dims(img_input, axis=0)  # BxCxHxW

    print(f"[DEBUG] Shape da entrada: {img_input.shape}")

    # === INFERÊNCIA ===
    start = time.time()
    output = SESSION.run([output_name], {input_name: img_input})[0]
    end = time.time()

    print(f"[DEBUG] Shape da saída: {output.shape}")
    print(f"[INFO] Tempo de inferência: {end - start:.3f} s")
    pred = output[0]  # (num_dets, 6)
    return pred, ratio, dwdh


def get_pecas(img: MatLike) -> list:
    logging.info("predizendo imagem")

    pred, ratio, (dw, dh) = get_predict(img)
    logging.info(f"{pred.shape[0]} detecções brutas")

    pecas = []
    for det in pred:
        if det[4] < 0.5:
            continue
        pecas.append(Peca(det, dw, dh, ratio))

    logging.info(f"encontrado {len(pecas)} peças confiáveis")
    return pecas


def get_matrix(pecas, slot):
    zeros_matrix = np.zeros((8, 8), dtype=int)
    frame_matrix = zeros_matrix.copy()

    for peca in pecas:
        m_x = int(peca.x / slot[0])
        m_y = int(peca.y / slot[1])
        frame_matrix[m_x, m_y] = 1

    return frame_matrix


def get_command(modify_frame):
    ALFABHETIC = ["a", "b", "c", "d", "e", "f", "g", "h"]

    old = np.where(modify_frame == 1)
    old = old[0][0], old[1][0]
    old = f"{ALFABHETIC[old[1]]}{old[0]+1}"
    new = np.where(modify_frame == -1)
    new = new[0][0], new[1][0]
    new = f"{ALFABHETIC[new[1]]}{new[0]+1}"
    command = f"{old}{new}"
    return command


def get_area(pecas):
    max_peca = max(pecas)
    min_peca = min(pecas)

    x = min_peca.x - int(min_peca.w / 2)
    w = max_peca.x - min_peca.x + max_peca.w
    y = min_peca.y - int(min_peca.h / 2)
    h = max_peca.y - min_peca.y + min_peca.h
    area_utilizavel = (x, y, w, h)
    return area_utilizavel
