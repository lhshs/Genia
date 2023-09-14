from tensorflow.keras.applications import VGG16
from tensorflow.keras.models import Model


def _get_model():
    # Load pre-trained VGG16 model
    base_model = VGG16(weights='imagenet')
    model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)

    return model