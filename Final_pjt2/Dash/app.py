import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
from moviepy.editor import VideoFileClip

from data import DataProcessor
from figure import FigureGenerator


# Initialize DataProcessor and FigureGenerator
data_processor = DataProcessor()
figure_generator = FigureGenerator('dev/Top_Lecture/', 'SON', 'dev/Other_Lecture/', 'BYUN')


# Get the figures
word_freq = figure_generator.word_freq()
senti = figure_generator.sentence_senti()
ng = figure_generator.n_grams()
pos = figure_generator.pos()
sim = figure_generator.similar()

app = dash.Dash()
app.layout = html.Div([
    html.H1('Video Analysis', style={'textAlign': 'center'}),
    html.Br(),
    dcc.Dropdown(
        id='nlp-feature-dropdown',
        options=[
            {'label': 'Word Frequency', 'value': 'word_freq'}, # NLP Feature 1
            {'label': 'Sentimental', 'value': 'senti'}, # NLP Feature 2
            {'label': 'Bigram', 'value': 'ng'}, # NLP Feature 3
            {'label': 'Part of Speech Tagging', 'value': 'pos'}, # NLP Feature 4
            {'label': 'Similarity', 'value': 'sim'}, # NLP Feature 5
        ],
        value='word_freq'
    ),
    dcc.Graph(id='nlp-feature-graph',
              style = {'display': 'inline-block', 
                       'width': '100%',
                       'height': '800px',
                    #    'fontsize' : 30
                       }
              ),
])

@app.callback(
    Output('nlp-feature-graph', 'figure'),
    Input('nlp-feature-dropdown', 'value')
)
def update_graph(selected_feature):
    if selected_feature == 'word_freq':
        return word_freq
    elif selected_feature == 'senti':
        return senti
    elif selected_feature == 'ng':
        return ng
    elif selected_feature == 'pos':
        return pos
    elif selected_feature == 'sim':
        return sim

if __name__ == '__main__':
    app.run_server(port=80, debug=True)
    