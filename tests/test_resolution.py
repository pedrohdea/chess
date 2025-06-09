import cv2
from loguru import logger


def testar_resolucoes(device=0):
    resolucoes = [
        (160, 120),
        (320, 240),
        (640, 360), # único funcional
        (640, 480),
        (800, 600),
        (1024, 768),
        (1280, 720),
        (1280, 960),
        (1280, 1024),
        (1600, 1200),
        (1920, 1080),
    ]

    cap = cv2.VideoCapture(device, cv2.CAP_V4L2)  # use CAP_V4L2 no Linux

    if not cap.isOpened():
        logger.debug("Erro ao abrir a câmera.")
        return

    logger.debug("Testando resoluções...\n")
    for largura, altura in resolucoes:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, largura)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, altura)
        real_largura = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        real_altura = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        suportada = int(real_largura) == largura and int(real_altura) == altura
        status = "✓ Suportada" if suportada else "✗ Ignorada"
        logger.debug(
            f"{largura}x{altura} -> Real: {int(real_largura)}x{int(real_altura)}   {status}"
        )

        ret, frame = cap.read()

        cv2.imshow(f"Webcam {largura}x{altura}", frame)

        # Pressione 'q' para sair
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()


testar_resolucoes()
