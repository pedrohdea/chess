from ultralytics import YOLO

model = YOLO("runs/detect/train3/weights/best.pt")
model.export(format="onnx", nms=True, half=False, simplify=False)
