# 정규 표현식 패키지
import re

# 토크나이저 패키지 
from nltk.tokenize import word_tokenize
from ckonlpy.tag import Twitter
from konlpy.tag import Kkma

from tokenizers import Tokenizer
from nltk.tokenize import RegexpTokenizer

# 벡터화 패키지
from sklearn.feature_extraction.text import TfidfVectorizer

# 분류 모델 패키지
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier

from xgboost import XGBClassifier

# 분류 모델 평가
from sklearn.metrics import classification_report

# 데이터 핸들링 
import numpy as np
import pandas as pd

# 기타
from tqdm import tqdm 


class UserTokenizers :
    def __init__(self) -> None :
        self.okt = Twitter()
        self.kkma = Kkma()
        self.bpe_tokenier_pretrained = Tokenizer.from_file('./tokenizer_data/bpe_tokenizer.json')

    @staticmethod
    def whitespaceTokenizer(data : str) -> list :
        token_rs = data.split(' ')
        return token_rs
    
    @staticmethod
    def regexsplitToken(data : str, pat : str = '[\,\.!?\n]') -> list :
        re_rs = re.split(pat, data, maxsplit=0)
        token_rs = [rs_unit.strip() for rs_unit in re_rs if len(rs_unit.strip()) > 1]
        return token_rs
    
    @staticmethod
    def regexselectToken(data : str, pat : str = '[\w]+') -> list :
        token_rs = RegexpTokenizer(pat).tokenize(data)
        return token_rs
    
    def BPETokenizer(self, data : str) -> list :
        token_rs = self.bpe_tokenier_pretrained.encode(data).tokens
        return token_rs
    
    # 한글, 영어 같이 사용
    def tokenizingKorEng(self, data : str) -> list :
        kor_re = re.findall('[ㄱ-ㅎㅏ-ㅣ가-힣]+', data)
        kor_str = ' '.join(kor_re)

        eng_re = re.findall('[a-zA-Z]+', data)
        eng_str = ' '.join(eng_re)

        kor_rs = self.kot.morphs(kor_str)
        eng_rs = word_tokenize(eng_str)

        token_rs = kor_rs + eng_rs

        return token_rs
    
    # 명사만 뽑는 tokenizer
    def konlpyNounsTokenizer(self, data : str) -> list : 
        token_rs = self.kkma.nouns(data)
        return token_rs