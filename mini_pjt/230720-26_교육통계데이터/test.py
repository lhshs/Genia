from dash import Dash, html, dcc, Input, Output, callback
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic')  
plt.rcParams['axes.unicode_minus'] = False
from statannot import add_stat_annotation
import warnings
warnings.filterwarnings('ignore')
import folium
import webbrowser
import plotly.express as px
import json
import ipywidgets
from IPython.display import HTML, display


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)


ori = pd.read_csv('data/18_22edustats.csv')

# app.layout = html.ori

if __name__ == '__main__':
    app.run(debug=True)


