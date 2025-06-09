import time
import numpy as np
import onnxruntime as ort
from loguru import logger

# === CONFIGURAÇÕES ===
MODEL_PATH = "runs/detect/train2/weights/best.onnx"

# Dummy input para exemplo — substitua pelo real!
def get_sample_input(session):
    input_name = session.get_inputs()[0].name
    input_shape = session.get_inputs()[0].shape
    input_shape = [dim if isinstance(dim, int) else 1 for dim in input_shape]
    input_data = np.random.rand(*input_shape).astype(np.float32)
    return {input_name: input_data}

def measure_inference(session):
    input_data = get_sample_input(session)
    start = time.time()
    output = session.run(None, input_data)
    end = time.time()
    return end - start

# Teste com CPU
session_cpu = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
cpu_time = measure_inference(session_cpu)
logger.debug(f"⏱️ CPUExecutionProvider: {cpu_time:.4f} segundos")

# Teste com OpenVINO
session_vino = ort.InferenceSession(MODEL_PATH, providers=["OpenVINOExecutionProvider"])
vino_time = measure_inference(session_vino)
logger.debug(f"⚡ OpenVINOExecutionProvider: {vino_time:.4f} segundos")

# Teste com CUDAExecutionProvider
# pip install onnxruntime-gpu
# Não funcionou, especifico para nvidia

# Teste com DirectMLExecutionProvider
# pip install onnxruntime-directml
# Não funcionou, versão do Python impede
