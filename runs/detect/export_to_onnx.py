from ultralytics import YOLO

model = YOLO("runs/detect/train2/weights/best.pt")
model.export(format="onnx", nms=True)
