import nltk    
import pandas as pd
from nltk.tokenize import word_tokenize

import s3


def first_data(route, first, configure='GPT'):
    '''
    Extract First Text Data
    '''
    first = s3.extract(route, first, configure)
    return first

def second_data(route, second, configure='GPT'):
    '''
    Extract Second Text Data
    '''
    second = s3.extract(route, second, configure)
    return second


def text_preprocess(first, second):
    ''' 
    Preprocess Text Data
    ''' 
    nltk.download('punkt')
    nltk.download('stopwords')
    stop_words = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에',
                '와','한','하다', '.', ',', '(', ')', '!', '?', '-', '‘', '’', '“', '”', '…', '텍스트는',
                '그리고', '그래서', '설명합니다', '중요성을 강조합니다', '논의합니다', '합니다', '있습니다', '있는', '있으며']
    word_tokens_lecture = word_tokenize(first.lower())
    filtered_top = [word for word in word_tokens_lecture if word.isalpha() and word not in stop_words]
    # Preprocess the lecture_bottom data
    word_tokens_lecture_bottom = word_tokenize(second.lower())
    filtered_other = [word for word in word_tokens_lecture_bottom if word.isalpha() and word not in stop_words]

    return filtered_top, filtered_other


