import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import base64
import io

import pandas as pd
import plotly.express as px
from moviepy.editor import VideoFileClip
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import plotly.express as px
import plotly.graph_objects as go
from matplotlib import pyplot as plt
import pandas as pd
import networkx as nx
import tempfile

import figure
import data
first = data.first_data('dev/Top_Lecture/', 'SON')
second = data.second_data('dev/Other_Lecture/', 'BYUN')

word_freq = figure.word_freq(first, second)
word_cloud = figure.word_cloud(first, second)

app = dash.Dash()
app.layout = html.Div([
    # Title
    html.Div(
        children=[
            html.H1('Video Analysis',
                    style={'textAlign': 'center'}),
        ]),
    html.Br(),
    html.Br(),
    # NLP_feature 1
    html.Div(id='NLP_feature 1',
             children=[
                 dcc.Graph(id='NLP_graph1',
                           figure=word_freq)
             ]),       
    html.Div(id='NLP_feature 2',
             children=[
                 dcc.Graph(id='NLP_graph2',
                           figure=word_cloud)
             ]),                                                         

])


if __name__ == '__main__':
    app.run_server(port=80, debug=True)