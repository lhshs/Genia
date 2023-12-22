import os 
from sqlalchemy import create_engine
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


host = os.environ.get("USER_HOST")
user = os.environ.get("USER_ID")
password = os.environ.get("USER_PASSWORD")
database = os.environ.get("USER_DB")
port = 3306

engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
)

def pie_em():
    table_name = 'VIDEO_FEATURE_EM'
    query = f"SELECT * FROM {table_name};"
    df = pd.read_sql(query, engine)
    
    df.loc[df['teacher']=='손석민', 'Count_Sentiment'] = df[df['teacher']=='손석민'].drop(columns=['teacher', 'book_name']).sum(axis=1)
    df.loc[df['teacher']=='변창현', 'Count_Sentiment'] = df[df['teacher']=='변창현'].drop(columns=['teacher', 'book_name']).sum(axis=1)
    df.loc[df['teacher']=='서채은', 'Count_Sentiment'] = df[df['teacher']=='서채은'].drop(columns=['teacher', 'book_name']).sum(axis=1)
    cat = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise']
    total_counts1 = df[df['teacher'] == '손석민'].drop(columns=['id', 'tot_frame', 'detect_frame', 'proba', 'no_proba', 'teacher',
                                                             'book_name', 'lecture_num', 'Count_Sentiment']).sum()
    total_counts2 = df[df['teacher'] == '변창현'].drop(columns=['id', 'tot_frame', 'detect_frame', 'proba', 'no_proba', 'teacher',
                                                             'book_name', 'lecture_num', 'Count_Sentiment']).sum()
    total_counts3 = df[df['teacher'] == '서채은'].drop(columns=['id', 'tot_frame', 'detect_frame', 'proba', 'no_proba', 'teacher',
                                                             'book_name', 'lecture_num', 'Count_Sentiment']).sum()
    total1 = total_counts1.sum()
    total2 = total_counts2.sum()
    total3 = total_counts3.sum()
    percentages1 = total_counts1 / total1
    percentages2 = total_counts2 / total2
    percentages3 = total_counts3 / total3

    fig = go.Figure()
    fig = make_subplots(rows=1, cols=3, subplot_titles=["<b>Top<b>", "<b>Other1<b>", "<b>Other2<b>"], specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=cat, values=round(percentages1, 3), name='Top Rank', hole=0.4,), row=1, col=1)
    fig.add_trace(go.Pie(labels=cat, values=round(percentages2, 3), name='Other Rank1', hole=0.4,), row=1, col=2)
    fig.add_trace(go.Pie(labels=cat, values=round(percentages3, 3), name='Other Rank2', hole=0.4,), row=1, col=3)

    return fig