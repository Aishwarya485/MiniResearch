from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(text_list):
    """
    Converts text chunks into vectors (numbers) so we can search semantically.
    """
    embeddings = model.encode(text_list, show_progress_bar=True)
    # Normalize for cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    embeddings = embeddings / norms
    return embeddings
