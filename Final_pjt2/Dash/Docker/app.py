import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from moviepy.editor import VideoFileClip
import base64
import io
import os 
import boto3
from datetime import datetime
import speech_recognition as sr

from data_s3 import DataProcessor
from figure_from_s3 import FigureGenerator
import figure_from_rds

import _s3

# Initialize & create global variables
data_processor = DataProcessor()
figures = {}

### ACCESS KEY FOR LOCAL ###
# import settings
# s3 = boto3.client('s3', 
#                 aws_access_key_id=settings.DB_SETTINGS['_s3']['ACCESS_KEY_ID'],
#                 aws_secret_access_key=settings.DB_SETTINGS['_s3']['ACCESS_SECRET_KEY'])
# transcribe = boto3.client('transcribe', 
#                         aws_access_key_id=settings.DB_SETTINGS['_s3']['ACCESS_KEY_ID'],
#                         aws_secret_access_key=settings.DB_SETTINGS['_s3']['ACCESS_SECRET_KEY'])
# bucket_name = settings.DB_SETTINGS['_s3']['BUCKET_NAME']

### ACCESS KEY FOR AWS, 환경변수 설정 ### 
s3 = boto3.client('s3', 
                  aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID"), 
                  aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY"))
bucket_name = os.environ.get("BUCKET_NAME")
filename = ''


app = dash.Dash()
app.layout = html.Div([

##### Title, First Web Scene #####    
    html.Br(),
    html.Br(),
    html.Div('Video Analysis', 
            style={'textAlign': 'center',
                   'fontSize': 70,
                   'fontFamily': 'Georgia',}),
    html.Br(),
    html.Div(
        dcc.Upload(
            id='upload-video',
            children=html.Div([
                'Drag and Drop or Select a Video',
            ]), 
            multiple=False,
            ),
            style={'display': 'flex', 
                   'justifyContent': 'center', 
                   'alignItems': 'center'}
            ),
    html.Br(),
    html.Div('Compare Videos About "NonVerbal Features" Of Top Lecture From EBS',
            id='subtitle'),
    html.Div(id='output-upload', ), 
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),    

###### Nonverbal Feature ######
    html.Div(
        children=[
            html.Div('< NonVerbal Feature >',
                     style={'display': 'none'},
                     id='nonverbal-feature-title'),
    # Face Detection 
            dcc.Graph(id='face-detection',
                      style = {'display': 'none'}),
    # Pie Emotion Chart
            dcc.Graph(id='pie-emotion',
                      style = {'display': 'none'}),                          
    # Pose Estimation
            dcc.Graph(id='pose-estimation',
                      style = {'display': 'none'}),
            ]),

    html.Br(),
    html.Br(),

###### Text Feature ######
    html.Div(
        children=[
            html.Div('< Verbal Feature >', 
                    style={'display': 'none'}, 
                    id='nlp-feature-title'
                    ),
            html.Br(),
            dcc.Dropdown(
                id='nlp-feature-dropdown',
                options=[
                    # NLP Feature 1
                    {'label': 'Word Frequency', 'value': 'word_freq'}, 
                    # NLP Feature 2
                    {'label': 'Sentence Sentimental Analysis', 'value': 'senti'}, 
                    # NLP Feature 3
                    {'label': 'Bigram', 'value': 'ng'}, 
                    # NLP Feature 4
                    {'label': 'Part of Speech Tagging', 'value': 'pos'}, 
                    # NLP Feature 5
                    {'label': 'Similarity', 'value': 'sim'}, 
                        ],
                        value='Select',
                        style={'display': 'none'}
                        ),
    # NLP Feature Graph
            ]),
    html.Div(
        children=[
            dcc.Graph(id='nlp-feature-graph',
                    style = {'width': '100%',
                            'height': '600px',
                            'display': 'none',
                            }
                     ),
                 ]
            ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
])

  
@app.callback(
        Output('output-upload', 'style'),
        Input('upload-video', 'contents')
        )
def upload_video(contents):
    if contents is not None:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        # Get current time and format it as a string
        # path = 'text/user/video/'
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        global filename
        filename = f'{current_time[:8]}_{current_time[8:]}_user_video.mp4'

        s3.upload_fileobj(io.BytesIO(decoded), bucket_name, filename)
        # Download the video from S3
        s3.download_file(bucket_name, filename, 'for_transcript_video.mp4')
        # Extract audio from video
        video = VideoFileClip('for_transcript_video.mp4')
        video.audio.write_audiofile('for_transcript_audio.wav')
        # Transcribe audio file into text
        r = sr.Recognizer() 
        with sr.AudioFile('for_transcript_audio.wav') as source: 
            audio = r.record(source) 
            text = r.recognize_google(audio, language="ko-KR") 
            # preprocess text
            text = data_processor.text_preprocess(text)
        # Save the transcript to a .txt file and upload it to S3
        transcript_file = io.BytesIO(' '.join(text).encode())
        print(transcript_file.getvalue().decode('utf-8')) # 적재된 데이터 확인
        s3.upload_fileobj(transcript_file, bucket_name, f'text/user/transcript/{current_time[:8]}_{current_time[8:]}_transcript.txt')
    return {'textAlign': 'center'}


def return_current_filename():
    global filename
    return filename


### See Graph After Upload Video ###
@app.callback(
        [
        Output('face-detection', 'figure'),
        Output('face-detection', 'style'),
        Output('pie-emotion', 'figure'),
        Output('pie-emotion', 'style'),
        # Output('pose-estimation', 'figure'),
        # Output('pose-estimation', 'style'),                
        ],
        Input('upload-video', 'contents')
)
def nonverbal_graph(selected_value):
    global filename
    filename = filename[:-4]
    # print(f'------------{filename}')
    face = figure_from_rds.face_esti('VIDEO_FEATURE_EM', 'USER_FM', filename)     
    pie = figure_from_rds.pie_em('VIDEO_FEATURE_EM', 'USER_EA')    
    # pose = figure_from_rds.pie_em('VIDEO_FEATURE_EM', 'USER_EA')    

    if selected_value is not None:
        return face, {'display': 'block'}, pie, {'display': 'block'} # pose, {'display': 'block'}, 
    else:
        return face, {'display': 'none'}, pie, {'display': 'none'} # pose, {'display': 'none'}, 


@app.callback(
        [
        Output('nlp-feature-graph', 'figure'),
        Output('nlp-feature-graph', 'style')
        ],
        Input('nlp-feature-dropdown', 'value')
)
def nlp_graph(selected_feature):
    print(f"<---- The Selected_Feature : {selected_feature} ---->")  # Debug print
    figure_generator = FigureGenerator('text/dev/Top_Lecture/', 'SON', 
                                        'text/dev/Other_Lecture/', 'BYUN',
                                        'text/dev/Other_Lecture/', 'SEO',
                                        'text/user/transcript/', _s3.get_most_recent_file(bucket_name, 'text/user/transcript/'))        
    word_freq = figure_generator.word_freq()
    senti = figure_generator.sentence_senti()
    ng = figure_generator.n_grams()
    pos = figure_generator.pos()
    sim = figure_generator.similar()

    if selected_feature == 'word_freq':
        return word_freq, {'display': 'block'}
    elif selected_feature == 'senti':
        return senti, {'display': 'block'}
    elif selected_feature == 'ng':
        return ng, {'display': 'block'}
    elif selected_feature == 'pos':
        return pos, {'display': 'block'}
    elif selected_feature == 'sim':
        return sim, {'display': 'block'}
    else:
        return word_freq, {'display': 'none'}


### DropDown Menu ###
@app.callback(
        [
        Output('nlp-feature-dropdown', 'style'),
        Output('nlp-feature-title', 'style')
        ],
        Input('upload-video', 'contents')
)
def show_dropdown(upload_output):
    if upload_output is not None:
        return {'display': 'block'}, \
               {'display': 'block', 
                'textAlign': 'center', 
                'fontFamily': 'Georgia', 
                'fontSize' : 30,
                'fontStyle': 'bold',
                'fontStyle': 'italic'}  
    else:
        return {'display': 'none'}, {'display': 'none'} 
    

@app.callback(
        [            
        Output('upload-video', 'style'),
        Output('subtitle', 'style'),        
        Output('nonverbal-feature-title', 'style'),
        ],
        Input('upload-video', 'contents')
)
def after_input_display(selected_value):
    if selected_value is not None:
        return {'display': 'none'}, \
               {'display': 'none'}, \
               {'display': 'block', 'textAlign': 'center', 
                'fontFamily': 'Georgia', 'fontSize' : 30,
                'fontStyle': 'bold', 'fontStyle': 'italic'} 
    else:
        return {'width': '110%', 'height': '80px', 'lineHeight': '80px',
                'borderWidth': '1px', 'borderStyle': 'dashed', 'borderRadius': '5px',
                'textAlign': 'center', 'margin': '10px'}, \
               {'textAlign': 'center', 'justifyContent': 'center', 
                'alignItems': 'center', 'fontSize': 15,
                'fontFamily': 'Lucida Console', 'fontStyle': 'italic'}, \
               {'display': 'none'} 


@app.callback(
        Output('output-upload', 'children'),
        Input('upload-video', 'contents')
        )
def update_output(contents):
    if contents is not None:
        video = html.Video(src=contents, controls=True)
        return video
    return html.Div()

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=80, debug=True) 
    