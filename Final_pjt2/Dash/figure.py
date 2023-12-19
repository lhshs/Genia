import nltk
from collections import Counter
import plotly.graph_objects as go
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.util import ngrams
import nltk
# nltk.download('vader_lexicon')
from plotly.subplots import make_subplots
from data import DataProcessor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import euclidean

class FigureGenerator:
    def __init__(self, first_route, first_name, 
                       second_route, second_name, 
                       user_route, user_name):
        self.data_processor = DataProcessor()
        self.first = self.data_processor.first_data(first_route, first_name)
        self.second = self.data_processor.second_data(second_route, second_name)
        self.user = self.data_processor.user_data(user_route, user_name)

    def process_text(self, text):
        return self.data_processor.text_preprocess(text)

    def create_word_freq_df(self, text):
        word_freq = Counter(self.process_text(text))
        df = pd.DataFrame.from_dict(word_freq, orient='index').reset_index()
        df = df.rename(columns={'index':'word', 0:'count'})
        df = df.sort_values(by='count', ascending=False).head(10)
        return df

    def word_freq(self):  
        '''
        Word Frequency
        '''
        df_first = self.create_word_freq_df(self.first)
        df_second = self.create_word_freq_df(self.second)
        df_user = self.create_word_freq_df(self.user)

        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_first['word'], y=df_first['count'], name='Top Rank Lecture'))
        fig.add_trace(go.Bar(x=df_second['word'], y=df_second['count'], name='Other Lecture'))
        fig.add_trace(go.Bar(x=df_user['word'], y=df_user['count'], name='Your Video'))
        fig.update_layout(barmode='group', title_text="<b>Top 10 Most Used Words<b>")
        return fig
    
    def sentence_senti(self):
        '''
        Sentiment Analysis
        '''
        sia = SentimentIntensityAnalyzer()

        sentences_top = nltk.sent_tokenize(self.first)
        positive = 0
        negative = 0
        neutral = 0
        for sentence in sentences_top:
            sentiment = sia.polarity_scores(sentence)
            if sentiment['compound'] > 0.05:
                positive += 1
            elif sentiment['compound'] < -0.05:
                negative += 1
            else:
                neutral += 1
        df_top_sent = pd.DataFrame({'sentiment': ['positive', 'negative', 'neutral'], 'count': [positive, negative, neutral]})

        sentences_bottom = nltk.sent_tokenize(self.second)
        positive_bottom = 0
        negative_bottom = 0
        neutral_bottom = 0
        for sentence in sentences_bottom:
            sentiment = sia.polarity_scores(sentence)
            if sentiment['compound'] > 0.05:
                positive_bottom += 1
            elif sentiment['compound'] < -0.05:
                negative_bottom += 1
            else:
                neutral_bottom += 1
        df_other_sent = pd.DataFrame({'sentiment': ['positive', 'negative', 'neutral'], 'count': [positive_bottom, negative_bottom, neutral_bottom]})

        sentences_bottom = nltk.sent_tokenize(self.user)
        positive_bottom = 0
        negative_bottom = 0
        neutral_bottom = 0
        for sentence in sentences_bottom:
            sentiment = sia.polarity_scores(sentence)
            if sentiment['compound'] > 0.05:
                positive_bottom += 1
            elif sentiment['compound'] < -0.05:
                negative_bottom += 1
            else:
                neutral_bottom += 1
        df_user_sent = pd.DataFrame({'sentiment': ['positive', 'negative', 'neutral'], 
                                     'count': [positive_bottom, negative_bottom, neutral_bottom]})

        fig = go.Figure()
        fig = make_subplots(rows=1, cols=3, 
                            specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]],
                            subplot_titles=['Top Lecture Sentences', 'Other Lecture Sentences', 'Your Sentences'])
        fig.add_trace(go.Pie(labels=df_top_sent['sentiment'], 
                     values=df_top_sent['count'], 
                     hole=.3,), row=1, col=1)
        fig.add_trace(go.Pie(labels=df_other_sent['sentiment'], 
                     values=df_other_sent['count'], 
                     hole=.3,
                     ), row=1, col=2)
        fig.add_trace(go.Pie(labels=df_user_sent['sentiment'], 
                     values=df_user_sent['count'], 
                     hole=.3), row=1, col=3)
        
        fig.update_layout(title_text="<b>Sentence Sentimental Analysis<b>")
        return fig
    
    def n_grams(self):
        '''
        N-grams
        '''
        # Top Lecture
        bigrams = list(ngrams(self.process_text(self.first), 5))
        bigram_freq = Counter(bigrams)
        df_bigrams_top = pd.DataFrame.from_dict(bigram_freq, orient='index').reset_index()
        df_bigrams_top = df_bigrams_top.rename(columns={'index':'bigram', 0:'count'})
        df_bigrams_top = df_bigrams_top.sort_values(by='count', ascending=False)
        # Other Lecture
        bigrams_bottom = list(ngrams(self.process_text(self.second), 5))
        bigram_freq_bottom = Counter(bigrams_bottom)
        df_bigrams_bottom = pd.DataFrame.from_dict(bigram_freq_bottom, orient='index').reset_index()
        df_bigrams_bottom = df_bigrams_bottom.rename(columns={'index':'bigram', 0:'count'})
        df_bigrams_bottom = df_bigrams_bottom.sort_values(by='count', ascending=False)
        # User Video
        bigrams_user = list(ngrams(self.process_text(self.user), 5))
        bigram_freq_user = Counter(bigrams_user)
        df_bigrams_user = pd.DataFrame.from_dict(bigram_freq_user, orient='index').reset_index()
        df_bigrams_user = df_bigrams_user.rename(columns={'index':'bigram', 0:'count'})
        df_bigrams_user = df_bigrams_user.sort_values(by='count', ascending=False)

        fig = go.Figure()
        fig.add_trace(go.Bar(x=df_bigrams_top['bigram'], y=df_bigrams_top['count'], name='Top Rank Lecture'))
        fig.add_trace(go.Bar(x=df_bigrams_bottom['bigram'], y=df_bigrams_bottom['count'], name='Other Lecture'))
        fig.add_trace(go.Bar(x=df_bigrams_user['bigram'], y=df_bigrams_user['count'], name='Your Video'))
        fig.update_layout(barmode='group', title_text="<b>Bigram Frequency<b>")
        fig.update_xaxes(title_text="")
        fig.update_yaxes(title_text="")
        return fig


    def pos(self):
        '''
        Part of Speech (POS) Tagging
        '''
        pos_tags = nltk.pos_tag(self.process_text(self.first))
        df_tag_top = pd.DataFrame(pos_tags, columns=['word', 'POS'])
        # Create a mapping dictionary
        pos_mapping = {'NNP': 'Proper Noun,<br>Singular', 
                    'NN': 'Noun,<br>Singular or Mass', 
                    'VB': 'Verb,<br>Base Form', 
                    'VBZ': 'Verb,<br>3rd person<br>Singular Present', 
                    'JJ': 'Adjective', 
                    'DT': 'Determiner', 
                    'IN': 'Preposition'} 
        color_mapping = {'Proper Noun,<br>Singular': 'blue'}
        # Top Lectture
        df_tag_top['POS'] = df_tag_top['POS'].replace(pos_mapping)
        df_tag_top['count'] = df_tag_top.groupby('POS')['POS'].transform('count') # Count the frequency of each POS
        df_tag_top = df_tag_top.sort_values(by='count', ascending=False).drop_duplicates() # Sort by count
        df_tag_top1 = df_tag_top[df_tag_top['count'] > 1000]  
        df_tag_top2 = df_tag_top[df_tag_top['count'] <= 1000]  
        # Other Lecture
        pos_tags_bottom = nltk.pos_tag(self.process_text(self.second))
        df_tag_bottom = pd.DataFrame(pos_tags_bottom, columns=['word', 'POS'])
        df_tag_bottom['POS'] = df_tag_bottom['POS'].replace(pos_mapping)
        df_tag_bottom['count'] = df_tag_bottom.groupby('POS')['POS'].transform('count')
        df_tag_bottom = df_tag_bottom.sort_values(by='count', ascending=False).drop_duplicates()
        df_tag_bottom1 = df_tag_bottom[df_tag_bottom['count'] > 1000]
        df_tag_bottom2 = df_tag_bottom[df_tag_bottom['count'] <= 1000]
        # User Video
        pos_tags_user = nltk.pos_tag(self.process_text(self.user))
        df_tag_user = pd.DataFrame(pos_tags_user, columns=['word', 'POS'])
        df_tag_user['POS'] = df_tag_user['POS'].replace(pos_mapping)
        df_tag_user['count'] = df_tag_user.groupby('POS')['POS'].transform('count')
        df_tag_user = df_tag_user.sort_values(by='count', ascending=False).drop_duplicates()
        df_tag_user1 = df_tag_user[df_tag_user['count'] > 1000]
        df_tag_user2 = df_tag_user[df_tag_user['count'] <= 1000]
        
        # Group by 'POS' and calculate the mean of 'count'
        df_tag_top1_grouped = df_tag_top1.groupby('POS', as_index=False)['count'].mean()
        df_tag_top2_grouped = df_tag_top2.groupby('POS', as_index=False)['count'].mean()
        df_tag_top2_grouped = df_tag_top2_grouped.sort_values('count', ascending=False)
        df_tag_bottom1_grouped = df_tag_bottom1.groupby('POS', as_index=False)['count'].mean()
        df_tag_bottom2_grouped = df_tag_bottom2.groupby('POS', as_index=False)['count'].mean()
        df_tag_bottom2_grouped = df_tag_bottom2_grouped.sort_values('count', ascending=False)
        df_tag_bottom2_grouped = df_tag_bottom2_grouped.head(5)
        df_tag_user1_grouped = df_tag_user1.groupby('POS', as_index=False)['count'].mean()
        df_tag_user2_grouped = df_tag_user2.groupby('POS', as_index=False)['count'].mean()
        df_tag_user2_grouped = df_tag_user2_grouped.sort_values('count', ascending=False)
        # df_tag_user2_grouped = df_tag_user2_grouped.head(5)        

        # Create subplot with two y-axes
        fig = make_subplots(rows=2, cols=3)
        fig.add_trace(go.Bar(x=df_tag_top1_grouped['POS'], y=df_tag_top1_grouped['count'], text=df_tag_top1_grouped['count'], 
                            textposition='auto', marker_line_width=0), row=1, col=1) 
        fig.add_trace(go.Bar(x=df_tag_top2_grouped['POS'], y=df_tag_top2_grouped['count'], text=df_tag_top2_grouped['count'], 
                            textposition='auto', marker_line_width=0), row=2, col=1)
        fig.add_trace(go.Bar(x=df_tag_bottom1_grouped['POS'], y=df_tag_bottom1_grouped['count'], text=df_tag_bottom1_grouped['count'], 
                            textposition='auto', marker_line_width=0), row=1, col=2)
        fig.add_trace(go.Bar(x=df_tag_bottom2_grouped['POS'], y=df_tag_bottom2_grouped['count'], text=df_tag_bottom2_grouped['count'], 
                            textposition='auto', marker_line_width=0), row=2, col=2)
        fig.add_trace(go.Bar(x=df_tag_user1_grouped['POS'], y=df_tag_user1_grouped['count'], text=df_tag_user1_grouped['count'], 
                            textposition='auto', marker_line_width=0), row=1, col=3)
        fig.add_trace(go.Bar(x=df_tag_user2_grouped['POS'], y=df_tag_user2_grouped['count'], text=df_tag_user2_grouped['count'],
                            textposition='auto', marker_line_width=0), row=2, col=3)
        
        fig.update_layout(title_text="<b>Part of Speech Tagging<b>")  # height=1200, width=800, 
        fig.update_layout(showlegend=False)
        return fig
    
    def similar(self):
        ncic = self.data_processor.second_data('dev/NCIC/', 'NCIC')
        # Convert the texts into TF-IDF features
        vectorizer = TfidfVectorizer().fit_transform([ncic, self.first, self.second, self.user])
        vectors = vectorizer.toarray()
        # Compute the cosine similarity
        cosine_sim = cosine_similarity(vectors)
        # Compute the Euclidean distance
        euclidean_distance_ncic_first = euclidean(vectors[0], vectors[1])
        euclidean_distance_ncic_second = euclidean(vectors[0], vectors[2])
        euclidean_distance_ncic_user = euclidean(vectors[0], vectors[3])
        # Plot the results
        labels = ['NCIC-Top_Lecture', 'NCIC-Other_Lecture', 'NCIC-User']
        cosine_values = [cosine_sim[0][1], cosine_sim[0][2], cosine_sim[0][3]]
        euclidean_values = [euclidean_distance_ncic_first, euclidean_distance_ncic_second, euclidean_distance_ncic_user]
        fig = go.Figure(data=[
            go.Bar(name='Cosine Similarity', x=labels, y=cosine_values),
            go.Bar(name='Euclidean Distance', x=labels, y=euclidean_values)
        ])
        # Change the bar mode
        fig.update_layout(barmode='group', title_text='Comparison Between NCIC, Top Rank Lecture and Other Rank Lecture and Your Video')
        return fig