import cv2
import numpy as np
import onnxruntime as ort
import time
import os
from engine.draw import draw_squares, letterbox

# === EXIBIÇÃO ===
os.environ["QT_QPA_PLATFORM"] = "xcb"  # evita conflitos no Linux

# === CONFIGURAÇÕES ===
MODEL_PATH = "runs/detect/train2/weights/best.onnx"
INPUT_SIZE = 640

# === INICIALIZA MODELO ONNX ===
print("[INFO] Carregando modelo ONNX...")
session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
input_name = session.get_inputs()[0].name
output_name = session.get_outputs()[0].name
print(f"[DEBUG] Nome do input: {input_name}")
print(f"[DEBUG] Nome do output: {output_name}")

# === INICIALIZA WEBCAM ===
print("[INFO] Iniciando webcam...")
cap = cv2.VideoCapture(0)
time.sleep(2)

if not cap.isOpened():
    raise RuntimeError("Erro ao abrir a webcam.")

print("Pressione 'q' para sair.\n")

try:
    while True:
        input("\nnext?\n")
        time.sleep(1)
        ret, frame = cap.read()
        if not ret:
            print("[ERRO] Frame não capturado.")
            break

        img, ratio, dwdh = letterbox(frame, (INPUT_SIZE, INPUT_SIZE))
        img_input = img.astype(np.float32) / 255.0
        img_input = np.transpose(img_input, (2, 0, 1))  # HWC → CHW
        img_input = np.expand_dims(img_input, axis=0)  # BxCxHxW

        print(f"[DEBUG] Shape da entrada: {img_input.shape}")

        # === INFERÊNCIA ===
        start = time.time()
        output = session.run([output_name], {input_name: img_input})[0]
        end = time.time()

        print(f"[DEBUG] Shape da saída: {output.shape}")
        print(f"[INFO] Tempo de inferência: {end - start:.3f} s")

        # === PÓS-PROCESSAMENTO ===
        pred = output[0]  # (num_dets, 6)
        frame = draw_squares(pred, frame, ratio, dwdh)

        # === EXIBIÇÃO ===
        # fps = 1 / (end - start)
        # # cv2.putText(
        # #     frame,
        # #     f"FPS: {fps:.1f}",
        # #     (10, 20),
        # #     cv2.FONT_HERSHEY_SIMPLEX,
        # #     0.6,
        # #     (0, 255, 0),
        # #     2,
        # # )
        cv2.imshow("YOLO ONNX Webcam", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

finally:
    cap.release()
    cv2.destroyAllWindows()
    print("\n[INFO] Encerrado com sucesso.")
