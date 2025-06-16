from imageai.Detection.Custom import DetectionModelTrainer

trainer = DetectionModelTrainer()
trainer.setModelTypeAsYOLOv3()
trainer.setDataDirectory(data_directory="positivas")

trainer.setTrainConfig(
    object_names_array=["gato"],
    batch_size=4,
    num_experiments=20,
    train_from_pretrained_model="gato-yolo.h5",
)

trainer.trainModel()

# https://www.instructables.com/Haar-Cascade-Python-OpenCV-Treinando-E-Detectando-/
