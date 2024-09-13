from tensorflow.keras.models import load_model as tf_load_model

def get_model(path):
    return tf_load_model(path)
