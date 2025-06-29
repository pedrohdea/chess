import logging
import time

import cv2
import numpy as np
import onnxruntime as ort
from cv2 import UMat
from cv2.typing import MatLike
from loguru import logger

from engine.draw import draw_squares, letterbox
from engine.model import Peca

# Cria a sessão ONNX com OpenVINO
# === CONFIGURAÇÕES ===
DEBUG = True
INPUT_SIZE = 640
CONFIDENCE = 0.3
MODEL_PATH = "runs/detect/train3/weights/best.onnx"
SESSION = ort.InferenceSession(
    MODEL_PATH, providers=["OpenVINOExecutionProvider", "CPUExecutionProvider"]
)

input_name = SESSION.get_inputs()[0].name
output_name = SESSION.get_outputs()[0].name


def get_predict(frame: UMat):
    img, ratio, dwdh = letterbox(frame, (INPUT_SIZE, INPUT_SIZE))
    img_input = img.astype(np.float32) / 255.0
    img_input = np.transpose(img_input, (2, 0, 1))
    img_input = np.expand_dims(img_input, axis=0)

    logger.debug(f"[DEBUG] Shape da entrada: {img_input.shape}")

    # === INFERÊNCIA ===
    start = time.time()
    output = SESSION.run([output_name], {input_name: img_input})[0]
    end = time.time()

    logger.debug(f"Shape da saída: {output.shape}")
    logger.debug(f"Tempo de inferência: {end - start:.3f} s")
    pred = output[0]  # (num_dets, 6)

    if DEBUG:
        frame = draw_squares(frame, pred, ratio, dwdh)
        cv2.imshow("DEBUG squares", frame)

    return pred, ratio, dwdh


def get_threshold(trust_list: list, qt_min: int) -> float:
    """
    Encontra o menor threshold necessário para obter pelo menos `min` detecções.

    Args:
        pred (np.ndarray): Detecções no formato [x1, y1, x2, y2, conf, cls]
        min (int): Número mínimo de detecções desejado
        max_thresh (float): Threshold inicial (começa do mais alto)
        min_thresh (float): Threshold mínimo permitido
        step (float): Decremento a cada iteração

    Returns:
        float: Threshold final encontrado
    """
    trust_list.sort()
    trust_list.reverse()
    threshold = min(trust_list[:qt_min])

    logger.debug(f"threshold {threshold}")
    if threshold < CONFIDENCE:
        threshold = CONFIDENCE

    return threshold


def get_pecas(pred, qt_min: int) -> list:
    logger.debug("Iniciando predição da imagem para encontrar peças...")

    if pred is None or len(pred) == 0:
        logger.debug("Nenhuma detecção bruta encontrada.")
        return []

    logger.debug(f"{pred.shape[0]} detecções brutas encontradas.")

    trust = [det[4] for det in pred]
    threshold = get_threshold(trust, qt_min)
    pecas = [Peca(det) for det in pred if det[4] >= threshold]

    logger.debug(f"Encontrado {len(pecas)} peças confiáveis após o threshold.")
    return pecas


def agrupar_valores_por_distribuicao(valores, grupos=8):
    valores_ordenados = sorted(valores)
    n = len(valores_ordenados)
    if n < grupos:
        raise ValueError("Número de valores insuficiente para agrupar.")

    diferencas = [valores_ordenados[i + 1] - valores_ordenados[i] for i in range(n - 1)]
    indices_corte = sorted(
        range(len(diferencas)), key=lambda i: diferencas[i], reverse=True
    )[: grupos - 1]
    indices_corte = sorted([i + 1 for i in indices_corte])
    limites = [0] + indices_corte + [n]

    grupos_resultado = []
    for i in range(len(limites) - 1):
        grupo = valores_ordenados[limites[i] : limites[i + 1]]
        media = int(sum(grupo) / len(grupo))
        grupos_resultado.append(media)

    return sorted(grupos_resultado)


def get_mapa(pecas):
    if not pecas:
        return np.zeros((8, 8), dtype=int)

    # Extrai centróides das peças
    centroides = [p.center for p in pecas]
    xs = [c[0] for c in centroides]
    ys = [c[1] for c in centroides]

    # Agrupa colunas com base na distribuição adaptativa (eixo X)
    colunas = agrupar_valores_por_distribuicao(xs, grupos=8)

    # Define linhas com espaçamento fixo com base na altura total (eixo Y)
    y_min = min(ys)
    y_max = max(ys)
    altura = y_max - y_min
    slot_h = altura / 7  # 7 intervalos → 8 casas

    linhas = [int(y_min + i * slot_h) for i in range(8)]

    # Calcula divisores entre casas
    meios_x = [(colunas[i] + colunas[i + 1]) // 2 for i in range(len(colunas) - 1)]
    meios_y = [(linhas[i] + linhas[i + 1]) // 2 for i in range(len(linhas) - 1)]
    return meios_x, meios_y


def get_matrix(pecas, mapa):
    meios_x, meios_y = mapa
    # Inicializa a matriz
    matrix = np.zeros((8, 8), dtype=int)

    # Preenche a matriz com base na posição de cada peça
    for p in pecas:
        cx, cy = p.center

        col = next((i for i, x in enumerate(meios_x) if cx < x), len(meios_x))
        row = next((i for i, y in enumerate(meios_y) if cy < y), len(meios_y))

        if 0 <= row < 8 and 0 <= col < 8:
            if matrix[row, col] == 1:
                logger.warning(f"[COLISÃO] Outra peça já estava em ({row}, {col})")
            matrix[row, col] = 1 if p.is_black else 3 # 1 = Black; 3 = White

    qtd_pecas = np.count_nonzero(matrix)
    if qtd_pecas == len(pecas):
        return matrix

    logger.warning("Matrix descartada, frame obstruído")
    return None


ALFABHETIC = ["a", "b", "c", "d", "e", "f", "g", "h"]
ALFABHETIC.reverse()

MOVE_PATTERNS = {
    "BM": (1, -1),
    "WM": (3, -3),
    "BC": (1, 2),
    "WC": (3, -2),
}

def validate_frame(modify_frame):
    """
    Valida a matriz de diferença e retorna o tipo de jogada detectada, se houver exatamente uma.

    Returns:
        str: Tipo de jogada ('BM', 'WM', 'BC', 'WC') se válida.
        None: Se nenhuma ou múltiplas jogadas válidas forem encontradas.
    """
    detected = []

    for move_type, (from_val, to_val) in MOVE_PATTERNS.items():
        if np.count_nonzero(modify_frame == from_val) == 1 and np.count_nonzero(modify_frame == to_val) == 1:
            detected.append(move_type)

    return detected[0] if len(detected) == 1 else None


def get_command(modify_frame):
    """
    Gera o comando de jogada a partir de uma matriz de diferença validada.

    Args:
        modify_frame (np.ndarray): matriz de diferença 8x8.
        return_type (bool): se True, retorna também o tipo de jogada.

    Returns:
        str: comando 'a2a3'
    """
    logger.debug('Procurando comando na matriz de diferença')

    move_type = validate_frame(modify_frame)
    if move_type is None:
        raise ValueError("Jogada inválida ou ambígua")

    from_val, to_val = MOVE_PATTERNS[move_type]

    from_pos = np.argwhere(modify_frame == from_val)[0]
    to_pos = np.argwhere(modify_frame == to_val)[0]

    from_coord = f"{ALFABHETIC[from_pos[1]]}{from_pos[0] + 1}"
    to_coord = f"{ALFABHETIC[to_pos[1]]}{to_pos[0] + 1}"
    command = f"{from_coord}{to_coord}"
    
    logger.debug(f'Comando encontrado na matriz de diferença {command}')

    return command
