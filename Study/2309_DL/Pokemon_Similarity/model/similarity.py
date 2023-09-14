import pickle
import os
from sklearn.metrics.pairwise import cosine_similarity

from data import load
from model import embedding, model



def similar_output(first_name, second_name):
    if 'feature_extraction.pickle' not in os.listdir():
        a_index = load.confirm().index(first_name)
        b_index = load.confirm().index(second_name)
        image_features = embedding.extract_features(load._data(), model._get_model())
        image1_features = list(image_features.values())[a_index]
        image2_features = list(image_features.values())[b_index]
        similarity = cosine_similarity(image1_features, image2_features)[0][0]
        similarity = str(round((similarity * 100), 2)) + '%'
        print('✨ RESULT✨')
        print(f"Similarity between\33[91m {first_name} \033[0mand\33[94m {second_name} \033[0m: {similarity}")
    
        # save feature extract dict
        with open('feature_extraction.pickle','wb') as fs:
            pickle.dump(image_features, fs)
    else:
        # load feature extract dict
        with open('feature_extraction.pickle', 'rb') as fl:
            image_features = pickle.load(fl)

        a_index = load.confirm().index(first_name)
        b_index = load.confirm().index(second_name)
        image1_features = list(image_features.values())[a_index]
        image2_features = list(image_features.values())[b_index]
        similarity = cosine_similarity(image1_features, image2_features)[0][0]
        similarity = str(round((similarity * 100), 2)) + '%'
        print('🔻 RESULT🔻')
        print(f"Similarity between\33[91m {first_name} \033[0mand\33[94m {second_name} \033[0m: {similarity}")
        
    return load.show_image(a_index, b_index)

