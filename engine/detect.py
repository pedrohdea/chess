import time

import cv2
from loguru import logger
from ultralytics import YOLO

MODEL_PATH = "runs/detect/train3/weights/best.pt"
MODEL = YOLO(MODEL_PATH)
DEBUG_MODE = True


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
    annotated_frame = frame.copy()

    # --- Inferência ---
    start_time = time.time()
    results = MODEL(annotated_frame)
    end_time = time.time()

    logger.debug(f"Tempo total de inferência YOLO: {end_time - start_time:.3f} s")

    # Extrai o primeiro (e geralmente único) objeto Results, pois processamos um único frame
    first_result = results[0]

    # Extrai os dados das detecções (bounding boxes, confiança, ID da classe)
    # Formato: [xmin, ymin, xmax, ymax, confidence, class_id]
    # Usamos .cpu().numpy() para converter o tensor PyTorch para um array NumPy na CPU
    detections_array = first_result.boxes.data.cpu().numpy()

    logger.debug(f"Número de detecções encontradas: {len(detections_array)}")

    if DEBUG_MODE:
        logger.debug(f"Shape do array de detecções: {detections_array.shape}")
        # Itera sobre cada detecção e desenha no frame
        for det in detections_array:
            # Coordenadas são inteiros para pixels
            xmin, ymin, xmax, ymax = map(int, det[:4])
            conf = det[4]
            class_id = int(det[5])  # Class ID é um inteiro

            # Define a cor do retângulo (verde)
            color = (0, 255, 0)
            thickness = 2

            # Desenha o retângulo
            cv2.rectangle(annotated_frame, (xmin, ymin), (xmax, ymax), color, thickness)

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
                annotated_frame,
                (text_x, text_y - text_size[1] - 5),
                (text_x + text_size[0] + 5, text_y + 5),
                color,
                1,
            )

            cv2.putText(
                annotated_frame,
                label,
                (text_x, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.4,
                (0, 0, 0),
                1,
                cv2.LINE_AA,
            )

    return detections_array, annotated_frame
