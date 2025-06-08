from ultralytics import YOLO
from cv2.typing import MatLike
from engine.model import Peca
import logging
import numpy as np


def get_vertice(box):
    vertices = box.data.tolist()[0]
    w = vertices[2] - vertices[0]
    h = vertices[3] - vertices[1]
    x = ((w) / 2) + vertices[0]
    y = ((h) / 2) + vertices[1]
    return int(x), int(y), int(w), int(h)


# MODEL = YOLO('yolov8n.pt')  # ou 'path/to/seu_modelo.pt'
onnx_model_path = "runs/detect/train2/weights/best.onnx"
MODEL = YOLO(onnx_model_path)

def get_predict(img: MatLike) -> list:
    logging.info('predizendo imagem')

    results = MODEL.predict(source=img)  # save predictions as labels
    logging.info(f'encontrado {len(results[0].boxes)}')

    pecas = []
    for box in results[0].boxes:
        vertice = get_vertice(box)
        peca = Peca()
        peca.vertice = vertice
        peca.multi = vertice[0] * vertice[1]
        pecas.append(peca)

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
    ALFABHETIC = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

    old = np.where(modify_frame == 1)
    old = old[0][0], old[1][0]
    old = f'{ALFABHETIC[old[1]]}{old[0]+1}'
    new = np.where(modify_frame == -1)
    new = new[0][0], new[1][0]
    new = f'{ALFABHETIC[new[1]]}{new[0]+1}'
    command = f'{old}{new}'
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
