import os
import random
import shutil
from sklearn.model_selection import KFold
from ultralytics import YOLO

# Configurações
dataset_dir = "dataset_dividido"
images_dir = os.path.join(dataset_dir, "images")
labels_dir = os.path.join(dataset_dir, "labels")
output_dir = "kfold_runs"
model_path = "yolov8n.pt"  # ou best.pt

k = 3
random.seed(42)

# Lista de imagens
image_files = [f for f in os.listdir(images_dir) if f.endswith(".jpg")]
random.shuffle(image_files)

# KFold
kf = KFold(n_splits=k)

for fold, (train_idx, val_idx) in enumerate(kf.split(image_files), 1):
    print(f"🔁 Rodando Fold {fold}/{k}")

    fold_dir = os.path.join(output_dir, f"fold{fold}")
    os.makedirs(fold_dir, exist_ok=True)

    for subset, indices in [("train", train_idx), ("val", val_idx)]:
        for tipo in ["images", "labels"]:
            os.makedirs(os.path.join(fold_dir, subset, tipo), exist_ok=True)

        for idx in indices:
            img = image_files[idx]
            lbl = img.replace(".jpg", ".txt")

            shutil.copy2(os.path.join(images_dir, img), os.path.join(fold_dir, subset, "images", img))
            shutil.copy2(os.path.join(labels_dir, lbl), os.path.join(fold_dir, subset, "labels", lbl))

    # Criar YAML
    data_yaml_path = os.path.join(fold_dir, "data.yaml")
    with open(data_yaml_path, "w") as f:
        f.write(f"path: {fold_dir}\n")
        f.write("train: train/images\n")
        f.write("val: val/images\n")
        f.write("names: ['class0']\n")  # Edite conforme suas classes

    # Treinar
    model = YOLO(model_path)
    model.train(data=data_yaml_path, epochs=50, project=fold_dir, name="results", exist_ok=True)

print("✅ K-Fold completo!")
