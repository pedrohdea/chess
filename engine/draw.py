import numpy as np
import cv2
from loguru import logger

# === FUNÇÕES AUXILIARES ===


def draw_squares(img, pred, ratio, dwdh):
    for det in pred:
        *xyxy, conf, cls = det
        if conf < 0.1:
            continue
        logger.debug(det)

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
            f"{conf:.2f}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )
    return img

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
