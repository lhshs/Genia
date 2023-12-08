import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import base64
import io
import psycopg2

import pandas as pd
import plotly.express as px

from moviepy.editor import VideoFileClip
import dash_table

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import plotly.express as px
from wordcloud import WordCloud
import plotly.graph_objects as go
from matplotlib import pyplot as plt
# plt.rcParams['font.family'] ='Malgun Gothic'
plt.rcParams['axes.unicode_minus'] =False
plt.rc('font', family='NanumGothic')
plt.rc('font', family='NanumBarunGothic')
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import networkx as nx

from Dash_Figure import Figure_Creator


app = dash.Dash()

figure_creator = Figure_Creator('./data/Iris.csv', './Lecture_Text/summarize/LECTURE_GPT_ALL_KOR_41672.txt')

app.layout = html.Div([
    # Title
    html.Div(
        children=[
            html.H1('Video Analysis',
                    style={'textAlign': 'center'}),
        ]),

    # Upload Video
    html.Div(
        dcc.Upload(
            id='upload-video',
            children=html.Div([
                'Drag and Drop or Select a Video',
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded        
            multiple=True,
        ),
        style={'display': 'flex', 'justifyContent': 'center', 'alignItems': 'center'}
    ),

    # Output Video
    html.Div(id='output-video',
             style={'display': 'flex', 
                    'justifyContent': 'space-around', 
                    'alignItems': 'center'}),
    
    html.Br(),
    html.Br(),

    # feature 1
    html.Div(id='feature1',
             children=[
                 html.H2('Face Detection And Mesh'),
                 dcc.Graph(id='NonVerbal_graph1')
             ]),
    html.Br(),

    # # feature 2
    # html.Div(id='feature2',
    #          children=[
    #              html.H2('Sentimental Analysis'),
    #              dcc.Graph(id='NonVerbal_graph2')
    #          ]),   

    # html.Br(),

    # # feature 3
    # html.Div(id='feature3',
    #          children=[
    #              html.H2('Pose Detection'),
    #              dcc.Graph(id='NonVerbal_graph3')
    #          ]),  

    # html.Br(),

    # # feature 4
    # html.Div(id='feature4',
    #          children=[
    #              html.H2('Face & Arm Detection'),
    #              dcc.Graph(id='NonVerbal_graph4')
    #          ]),   

    html.Br(),

    # NLP_feature 1
    html.Div(id='NLP_feature 1',
             children=[
                 html.H2('The Most Frequent Words'),
                 dcc.Graph(id='NLP_graph1'
                           )
             ]),   
    # # NLP_feature 2
    # html.Div(id='NLP_feature 2',
    #          children=[
    #              html.H2('Histogram Of Word Length'),
    #              dcc.Graph(id='NLP_graph2')
    #          ]),   
    # # NLP_feature 3
    # html.Div(id='NLP_feature 3',
    #          children=[
    #              html.H2('Heatmap Of Term Frequency'),
    #              dcc.Graph(id='NLP_graph3')
    #          ]),   
    # # NLP_feature 4
    # html.Div(id='NLP_feature 4',
    #          children=[
    #              html.H2('Network Diagram'),
    #              dcc.Graph(id='NLP_graph4')
    #          ]),                                           

])


@app.callback(
    Output('output-video', 'children'),
    Input('upload-video', 'contents'),
    prevent_initial_call=True
)
def side_data(list_of_contents):
    fig = None
    if list_of_contents is not None:
        for contents in list_of_contents:
            # The contents are base64 encoded, so we must decode them
            decoded = base64.b64decode(contents.split(',')[1])
            
            ########### Will Load to S3 ###########
            # Write the binary data to a file
            with open('./User_Upload/Input_Video.mp4', 'wb') as f:
                f.write(decoded)

            # Read the video file and extract metadata
            clip = VideoFileClip('./User_Upload/Input_Video.mp4')
            
            # Extract metadata
            duration = clip.duration
            fps = clip.fps
            size = str(clip.size)
            audio_fps = clip.audio.fps if clip.audio is not None else None
            audio_nchannels = clip.audio.nchannels if clip.audio is not None else None
        
            ########### About Side Table ###########
            # Create a DataFrame from the metadata
            df = pd.DataFrame({
                'Duration': [duration],
                'FPS': [fps],
                'Size': [size],
                'Audio FPS': [audio_fps],
                'Audio Channels': [audio_nchannels],
            })

            # Transpose the DataFrame
            df = df.transpose()
            df.columns = ['Value']            

            # Reset the index and rename the index column to 'Metadata'
            df = df.reset_index().rename(columns={'index': 'Metadata'})            

            # Create a DataTable from the DataFrame
            table = go.Figure(data=[go.Table(
                header=dict(values=list(df.columns),
                            fill_color='paleturquoise',
                            align='left'),
                cells=dict(values=[df.Metadata, df.Value],
                           fill_color='lavender',
                           align='left'))
            ])                

        children = [
            html.Div(
                children=[
                    html.Video(src=contents, 
                               controls=True, 
                               style={'width': '100%'})
                ],
                style={'width': '50%'}
            ),
            html.Div(
                children=[dcc.Graph(figure=table)],
                style={'width': '70%', 'alignItems': 'center'}
            )
        ]
        return children

@app.callback(
    Output('NonVerbal_graph1', 'figure'),
    Input('upload-video', 'contents'),
    prevent_initial_call=True
)
def update_graph(n):
    fig = None
    if n is not None:    
        fig = figure_creator.create_sample()
    return fig


@app.callback(
    Output('NLP_graph1', 'figure'),
    Input('upload-video', 'contents'),
    prevent_initial_call=True
)
def update_graph(n):
    fig = None
    if n is not None:    
        fig = figure_creator.create_bar()
    return fig
    

@app.callback(
    Output('NLP_graph2', 'figure'),
    Input('upload-video', 'contents'),
    prevent_initial_call=True
)
def update_graph(n):
    fig = None
    if n is not None:    
        fig = figure_creator.create_hist()
    return fig
    
    
@app.callback(
    Output('NLP_graph3', 'figure'),
    Input('upload-video', 'contents'),
    prevent_initial_call=True
)
def update_graph(n):
    fig = None
    if n is not None:    
        fig = figure_creator.create_heatmap()
    return fig
    
    
@app.callback(
    Output('NLP_graph4', 'figure'),
    Input('upload-video', 'contents'),
    prevent_initial_call=True
)
def update_graph(n):
    fig = None
    if n is not None:    
        fig = figure_creator.create_network()
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)