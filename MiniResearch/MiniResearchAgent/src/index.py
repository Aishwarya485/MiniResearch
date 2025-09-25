import faiss
import numpy as np

def build_faiss_index(embeddings):
    """
    Builds a FAISS index for fast similarity search
    """
    d = embeddings.shape[1]
    index = faiss.IndexFlatIP(d)  # Cosine similarity
    index.add(embeddings)
    return index
