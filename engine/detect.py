import time

import cv2
import numpy as np
from loguru import logger
from ultralytics import YOLO

from engine.model import Peca
from settings import conf

MODEL_PATH = "runs/detect/train3/weights/best.pt"
MODEL = YOLO(MODEL_PATH)
DEBUG_MODE = True


def draw_yolo(frame, det):
    # Coordenadas são inteiros para pixels
    xmin, ymin, xmax, ymax = map(int, det[:4])
    conf = det[4]
    class_id = int(det[5])  # Class ID é um inteiro

    # Define a cor do retângulo (verde)
    color = (0, 255, 0)
    thickness = 2

    # Desenha o retângulo
    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, thickness)

    # Prepara o texto do rótulo
    label = f"ID: {class_id} C: {conf:.2f}"

    # Posição do texto (acima do retângulo)
    text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.4, 1)[0]
    text_x = xmin
    text_y = (
        ymin - 10 if ymin - 10 > text_size[1] else ymin + text_size[1] + 5
    )  # Ajusta se muito perto da borda

    # Desenha o fundo do texto para melhor visibilidade
    cv2.rectangle(
        frame,
        (text_x, text_y - text_size[1] - 5),
        (text_x + text_size[0] + 5, text_y + 5),
        color,
        1,
    )

    cv2.putText(
        frame,
        label,
        (text_x, text_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.4,
        (0, 0, 0),
        1,
        cv2.LINE_AA,
    )
    return frame


def black_or_white(pecas):
    cores = [peca.gradiente for peca in pecas]
    # cores = [
    #     np.float64(94.65306122448979), np.float64(86.80590062111801), np.float64(171.44444444444446),
    # ]

    media_geral = np.mean(cores)
    std_geral = np.std(cores)

    brancas = [v for v in cores if v > media_geral]
    pretas = [v for v in cores if v <= media_geral]

    media_brancas = np.mean(brancas)
    std_brancas = np.std(brancas)
    media_pretas = np.mean(pretas)
    std_pretas = np.std(pretas)

    logger.debug(f"Média geral: {media_geral:.2f} | desvio padrão = {std_geral:.2f}")
    logger.debug(
        f"Brancas ({len(brancas)}): {media_brancas=:.2f} | desvio padrão = {std_brancas:.2f}"
    )
    logger.debug(
        f"Pretas  ({len(pretas)}): {media_pretas=:.2f} | desvio padrão = {std_pretas:.2f}"
    )

    if len(brancas) == len(pretas) == 16:
        conf.DIVISAODEGRADIENTE = media_geral


def get_piece_color(roi: np.ndarray) -> str:
    """
    Determina a cor da peça com base na média de brilho (canal V em HSV).
    """
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    v_mean = np.mean(hsv[:, :, 2])
    return v_mean


def get_color(peca: Peca, frame):
    x1, y1, x2, y2, conf, class_id = peca.det
    x1, y1, x2, y2 = map(int, [x1, y1, x2, y2])
    roi = frame[y1:y2, x1:x2]

    if roi.size == 0:
        return

    v_mean = get_piece_color(roi)
    peca.gradiente = v_mean


def get_pecas_colors(pecas, frame):
    for peca in pecas:
        get_color(peca, frame)

    black_or_white(pecas)


# --- Função get_predict ---
def get_yolo_detect(frame: cv2.UMat):
    """
    Realiza a inferência de detecção de objetos em um frame do OpenCV usando um modelo YOLOv8 (.pt).
    O pré-processamento, a inferência e o pós-processamento (incluindo NMS) são
    todos tratados internamente pela biblioteca Ultralytics.

    Args:
        frame (cv2.UMat): O frame de entrada do OpenCV.

    Returns:
        tuple: Uma tupla contendo:
            - detections_array (np.ndarray or None): Um array NumPy das detecções
              no formato [xmin, ymin, xmax, ymax, confidence, class_id] para cada objeto detectado.
              Retorna None se o frame for inválido ou não houver detecções.
            - annotated_frame (cv2.UMat): O frame original com os quadrados das detecções
              desenhados. Retorna o frame original sem anotações se DEBUG_MODE for False
              ou se não houver detecções.
    """
    # Certifique-se de que o frame é gravável se você for desenhar nele
    # OpenCV's UMat usually handles this, but for numpy arrays it's important.
    # No entanto, vamos criar uma cópia para garantir que o frame original não seja modificado
    # diretamente, caso ele seja usado em outro lugar.
    frame = frame.copy()

    # --- Inferência ---
    start_time = time.time()
    results = MODEL(frame, verbose=False)
    end_time = time.time()

    logger.debug(f"Tempo total de inferência YOLO: {end_time - start_time:.3f} s")

    # Extrai o primeiro (e geralmente único) objeto Results, pois processamos um único frame
    first_result = results[0]

    # Extrai os dados das detecções (bounding boxes, confiança, ID da classe)
    # Formato: [xmin, ymin, xmax, ymax, confidence, class_id]
    # Usamos .cpu().numpy() para converter o tensor PyTorch para um array NumPy na CPU
    detections = first_result.boxes.data.cpu().numpy()
    logger.debug(f"Número de detecções encontradas: {len(detections)}")

    if DEBUG_MODE:
        for det in detections:
            logger.debug(f"Shape do array de detecções: {detections.shape}")
            frame = draw_yolo(frame, det)

    return detections, frame
