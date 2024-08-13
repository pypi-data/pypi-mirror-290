import pandas as pd
import plotly.express as px


class Visualizer:
    def __init__(self, X, text, labels) -> None:
        self.X = X
        self.text = text
        self.labels = labels

    def show(self, labels_map=None):
        df = pd.DataFrame(self.X, columns=['TSNE1', 'TSNE2'])
        df["text"] = self.text

        kwargs_fig = {"x": "TSNE1", "y":"TSNE2", "hover_name":"text", "opacity":0.7}

        if self.labels is not None:
            df["labels"] = self.labels.astype(str)
            if labels_map is not None:
                df["labels_map"] = df["labels"].map(labels_map).fillna(df["labels"])
                kwargs_fig["color"] = "label_map"
            else:
                kwargs_fig["color"] = "label"
            kwargs_fig["color_discrete_sequence"] = px.colors.qualitative.Alphabet

        fig = px.scatter(df, **kwargs_fig)
        fig.update_traces(marker=dict(line=dict(width=0.2,
                                                color='DarkSlateGrey')),
                        selector=dict(mode='markers'))
        fig.update_layout(
            title="Hello",
            autosize=False,
            width=1400,
            height=800,
            xaxis_title="dimension 1",
            yaxis_title="dimension 2"
        )
        return fig