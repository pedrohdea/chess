import coremltools as ct
import numpy as np
import PIL.Image

# Load a model whose input type is "Image".
model = ct.models.MLModel("model.mlmodel")

Height = 20  # use the correct input image height
Width = 60  # use the correct input image width


# Scenario 1: load an image from disk.
def load_image(path, resize_to=None):
    # resize_to: (Width, Height)
    img = PIL.Image.open(path)
    if resize_to is not None:
        img = img.resize(resize_to, PIL.Image.Resampling.LANCZOS)
    img_np = np.array(img).astype(np.float32)
    return img_np, img


# Load the image and resize using PIL utilities.
_, img = load_image("positivas/greygato7.png", resize_to=(Width, Height))
out_dict = model.predict({"image": img})

# Scenario 2: load an image from a NumPy array.
shape = (Height, Width, 3)  # height x width x RGB
data = np.zeros(shape, dtype=np.uint8)
# manipulate NumPy data
pil_img = PIL.Image.fromarray(data)
out_dict = model.predict({"image": pil_img})
