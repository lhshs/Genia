import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import base64

import pandas as pd
from moviepy.editor import VideoFileClip

import plotly.graph_objects as go
import pandas as pd
import tempfile


app = dash.Dash()

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

            # Write the decoded video data to a temporary file
            with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmpfile:
                tmpfile.write(decoded)
                tmpfilepath = tmpfile.name

            # Read the video file from the temporary file
            clip = VideoFileClip(tmpfilepath)

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


if __name__ == '__main__':
    # app.run_server(port=80, debug=True)