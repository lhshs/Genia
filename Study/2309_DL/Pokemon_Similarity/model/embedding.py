from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
import numpy as np

from data import load



def extract_features(image_path, model):
    '''
    Input
        1) image_path: list()
            - 이미지 경로 list
        2) model
            - VGG16(weights='imagenet')
    Result
        image_path에 있는 image 파일을 vgg16 모델을 통해 feature extraction 
        1개씩 수행하며, 5개가 완료됐을 때 얼마나 수행됐는지 알려준다 
    '''
    image_features = {}
    print('🌈  Start Extract Image Feature 🌈')
    for _idx, _image in enumerate(image_path):
        img = image.load_img(_image, target_size=(224, 224))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        img = preprocess_input(img)
        features = model.predict(img, verbose=-1)
        image_features[_image] = features
        if (_idx+1) % 5 == 0:
            print(f'Extract {_idx+1} / {len(load._data())} ..ing')
    print('🥕 FINISH 🥕')
    
    return image_features

