import pandas as pd
import plotly.express as px
import nltk    

from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import networkx as nx
import plotly.graph_objects as go

from Dash_Data import Figure_Data


class Figure_Creator:
    def __init__(self, data_path, text_path):
        self.data = Figure_Data(data_path, text_path)

    # Sample Figure
    def create_sample(self):
        feature, processed_text = self.data.get_processed_data()
        fig = px.scatter(feature, x="SepalWidth", y="SepalLength", color="Species")
        return fig

    # Create a bar plot of the most frequent words
    def create_bar(self):
        feature, processed_text = self.data.get_processed_data()
        word_counts = Counter(processed_text)
        most_common_words = word_counts.most_common(10)
        fig = px.bar(x=[word[0] for word in most_common_words], y=[word[1] for word in most_common_words])
        return fig
    
    # Create a histogram of word length
    def create_hist(self):
        feature, processed_text = self.data.get_processed_data()
        word_lengths = [len(word) for word in processed_text]
        fig = px.histogram(x=word_lengths, nbins=max(word_lengths))
        return fig

    # Create a heatmap of term frequency
    def create_heatmap(self):
        feature, processed_text = self.data.get_processed_data()
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(processed_text)
        term_frequency = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())
        fig = px.imshow(term_frequency)
        return fig

    # Create a network diagram
    def create_network(self):
        feature, processed_text = self.data.get_processed_data()
        bigrams = nltk.bigrams(processed_text)
        bigram_freq = nltk.FreqDist(bigrams)
        bigram_df = pd.DataFrame(bigram_freq.items(), columns=["bigram", "freq"])
        bigram_df = bigram_df.sort_values(by="freq", ascending=False)

        G = nx.Graph()

        for index, row in bigram_df.iterrows():
            G.add_edge(row["bigram"][0], row["bigram"][1], weight=row["freq"])

        pos = nx.spring_layout(G)
        edge_x = []
        edge_y = []
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            marker=dict(
                showscale=True,
                colorscale='YlGnBu',
                reversescale=True,
                color=[],
                size=10,
                colorbar=dict(
                    thickness=15,
                    title='Node Connections',
                    xanchor='left',
                    titleside='right'
                ),
                line_width=2))

        node_adjacencies = []
        node_text = []
        for node, adjacencies in enumerate(G.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append('# of connections: '+str(len(adjacencies[1])))

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

        fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        # title='Network graph made with Python',
                        titlefont_size=16,
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20,l=5,r=5,t=40),
                        # annotations=[ dict(
                        #     showarrow=False,
                        #     xref="paper", yref="paper",
                        #     x=0.005, y=-0.002 ) ],
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                        )        

        return fig
