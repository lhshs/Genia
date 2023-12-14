import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import plotly.express as px
from wordcloud import WordCloud
import plotly.graph_objects as go
from matplotlib import pyplot as plt
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.util import ngrams
import spacy
import nltk
nltk.download('vader_lexicon')
from plotly.subplots import make_subplots
import data


# first = data.first_data('dev/Top_Lecture/', 'SON')
# second = data.second_data('dev/Other_Lecture/', 'BYUN')
# print(first[:100])
# print('-------------------')
# print(second[:100])


def word_freq(first, second):
    '''
    Word Frequency
    '''
    # Word Frequency for top_lecture
    word_freq_lecture = Counter(data.text_preprocess(first, second)[0])
    df_first = pd.DataFrame.from_dict(word_freq_lecture, orient='index').reset_index()
    df_first = df_first.rename(columns={'index':'word', 0:'count'})
    df_first = df_first.sort_values(by='count', ascending=False).head(10)
    # Word Frequency for other_lecture
    word_freq_other_lecture = Counter(data.text_preprocess(first, second)[1])
    df_second = pd.DataFrame.from_dict(word_freq_other_lecture, orient='index').reset_index()
    df_second = df_second.rename(columns={'index':'word', 0:'count'})
    df_second = df_second.sort_values(by='count', ascending=False).head(10)
    # Add other_lecture data to the word frequency graph
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_first['word'], y=df_first['count'], name='Top Rank Lecture'))
    fig.add_trace(go.Bar(x=df_second['word'], y=df_second['count'], name='Bottom Rank Lecture'))
    fig.update_layout(barmode='group', title_text="<b>Top 10 Word Frequency Comparison</b>")

    return fig

def word_cloud(first, second):
    '''
    Word Cloud
    ## Pillow==9.5.0
    '''
    # Word Cloud for lecture_top
    wordcloud = WordCloud(width = 1000, height = 500, 
                        background_color="white", 
                        font_path='C:\\Windows\\Fonts\\NGULIM.TTF'
                        ).generate(' '.join(data.text_preprocess(first, second)[0]))
    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    result1 = plt.show()

    # Word Cloud for lecture_bottom
    wordcloud = WordCloud(width = 1000, height = 500,
                        background_color="white", 
                        font_path='C:\\Windows\\Fonts\\NGULIM.TTF'
                        ).generate(' '.join(data.text_preprocess(first, second)[1]))
    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    result2 = plt.show()

    return result1, result2