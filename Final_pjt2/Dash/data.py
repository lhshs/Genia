import nltk    
import pandas as pd
from nltk.tokenize import word_tokenize
from collections import Counter

import s3


class DataProcessor:
    def __init__(self, configure='GPT'):
        self.configure = configure

    def first_data(self, route, first):
        '''
        Extract First Text Data
        '''
        first = s3.extract(route, first, self.configure)
        return first

    def second_data(self, route, second):
        '''
        Extract Second Text Data
        '''
        second = s3.extract(route, second, self.configure)
        return second
    
    def ncic(self, route, ncic):
        '''
        Extract NCIC Text Data
        '''
        ncic = s3.extract(route, ncic, self.configure)
        return ncic

    def text_preprocess(self, text):
        ''' 
        Preprocess Text Data
        ''' 
        nltk.download('punkt')
        nltk.download('stopwords')
        stop_words = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에',
                    '와','한','하다', '.', ',', '(', ')', '!', '?', '-', '‘', '’', '“', '”', '…', '텍스트는',
                    '그리고', '그래서', '설명합니다', '중요성을 강조합니다', '논의합니다', '합니다', '있습니다', '있는', '있으며',
                    '중요성을', '강조합니다', '대해', '수', '제공합니다', '대한', '방법을']
        word_tokens_lecture = word_tokenize(text.lower())
        filtered_text = [word for word in word_tokens_lecture if word.isalpha() and word not in stop_words]

        return filtered_text
    
    def word_frequnecy_list(self, text):
        '''
        Calculate word frequency for first and second data
        '''
        # Calculate word frequency
        word_freq_first = Counter(self.text_preprocess(self.first_data('dev/Top_Lecture/', 'SON')))
        word_freq_second = Counter(self.text_preprocess(self.second_data('dev/Other_Lecture/', 'BYUN')))

        # Convert to list
        word_freq_first_list = [list(x) for x in word_freq_first.items()]
        word_freq_first_list = sorted(word_freq_first_list, key=lambda x: x[1], reverse=True)
        word_freq_second_list = [list(x) for x in word_freq_second.items()]
        word_freq_second_list = sorted(word_freq_second_list, key=lambda x: x[1], reverse=True)

        return word_freq_first_list, word_freq_second_list    
    
