from typing import Optional

from sentence_transformers import SentenceTransformer
from transformers import PreTrainedModel

from ..utils import set_device, batch_embed
from ..embedder import STEmbedder, HFEmbedder
from ..visualizer import Visualizer, SklearnReducer


class Mbedder:
    def __init__(self, text: list[str], dev: Optional[str] = None) -> None:
        self.text = text
        self.embeddings = None
        self.embeddings_red = None
        self.labels = None
        self.dev = set_device(dev)


    def embed(self, model, *args, **kwargs):
        if isinstance(model, SentenceTransformer):
            embedder = STEmbedder(model, self.text)
        elif isinstance(model, PreTrainedModel):
            embedder = HFEmbedder(model, self.text)
        else:
            raise NotImplementedError
        
        self.embeddings = batch_embed(embedder, *args, dev=self.dev, **kwargs) # TODO convert to method of Embedder


    def reduce(self, model):
        if "sklearn" in str(type(model)):
            reducer = SklearnReducer(model)
        else:
            raise NotImplementedError
        
        self.embeddings_red = reducer.reduce(self.embeddings.cpu())
    

    def cluster(self, model):
        pass
    

    def show(self, reduce_model=None, cluster_model=None):
        if reduce_model is not None:
            self.reduce(reduce_model)
        if cluster_model is not None:
            self.cluster(cluster_model)

        if (self.embeddings_red is None) and (self.embeddings.shape[1] > 2):
            raise ValueError("Your embeddings have a dimensionality higher than 2 and can't be displayed on a plot. Please choose a dimensionality reduction method before.")
        if (self.embeddings_red.shape[1] > 2):
            raise ValueError("Your reduced embeddings have a dimensionality higher than 2 and can't be displayed on a plot. Please choose another dimensionality reduction method.")

        if self.embeddings_red is not None:
            visualizer = Visualizer(self.embeddings_red, self.text, self.labels)
        else:
            visualizer = Visualizer(self.embeddings, self.text, self.labels)
        return visualizer.show()
    
   