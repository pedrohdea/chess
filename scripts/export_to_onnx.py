from ultralytics import YOLO

model = YOLO("runs/detect/train3/weights/best.pt")
model.export(format="onnx", nms=True, half=False, simplify=False)
metrics = model.val()  # usa os dados definidos no .yaml do treinamento
print("mAP@0.5:", metrics.box.map50)
print("mAP@0.5:0.95:", metrics.box.map)
print("Precisão:", metrics.box.precision)
print("Recall:", metrics.box.recall)
