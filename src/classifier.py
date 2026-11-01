"""Leaf photo -> disease prediction (trained model)."""
import io
import json

import numpy as np
import tensorflow as tf
from PIL import Image

from . import config

model = tf.keras.models.load_model(config.MODEL_PATH)
class_names = json.load(open(config.CLASS_NAMES_PATH))


def _pretty(i):
    # "Tomato___Late_blight" -> "Tomato - Late blight"
    return class_names[i].replace("___", " - ").replace("_", " ").strip()


def diagnose(image_bytes, k=3):
    """Return the top-k predictions as [(disease, confidence), ...]."""
    size = (config.IMG_SIZE, config.IMG_SIZE)
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB").resize(size)
    # The saved model already contains MobileNetV2 preprocessing, so pass raw 0-255 pixels
    p = model.predict(np.asarray(img, dtype="float32")[None], verbose=0)[0]
    return [(_pretty(i), float(p[i])) for i in p.argsort()[::-1][:k]]
