import nltk    
import pandas as pd
import plotly.express as px
from nltk.tokenize import word_tokenize

class Figure_Data:

    def __init__(self, data_path, text_path):
        self.data_path = data_path
        self.text_path = text_path

    def fetch_data(self):
        feature = pd.read_csv(self.data_path)
        with open(self.text_path, 'r', encoding='utf-8') as file:
            txt = file.read()
        return feature, txt

    def preprocess_text(self):
        feature, txt = self.fetch_data()
        self.txt = txt
        nltk.download('punkt')
        nltk.download('stopwords')
        stop_words = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에',
                      '와','한','하다', '.', ',', '(', ')', '!', '?', '-', '‘', '’', '“', '”', '…', '텍스트는',
                      '그리고', '그래서']
        word_tokens = word_tokenize(txt.lower())
        filtered_text = [word for word in word_tokens if word.isalpha() and word not in stop_words]
        return filtered_text
    
    def get_processed_data(self):
        feature, txt = self.fetch_data()
        self.txt = txt
        processed_text = self.preprocess_text()
        return feature, processed_text



