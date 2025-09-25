import numpy as np
from src.embed import model

def retrieve(query, index, chunks, k=5):
    """
    Search for the top-k most relevant chunks for the query.
    Returns list of dictionaries: {'text','source','page','score'}
    """
    q_emb = model.encode([query])
    q_emb = q_emb / np.linalg.norm(q_emb, axis=1, keepdims=True)
    D, I = index.search(q_emb, k)
    results = []
    for idx, score in zip(I[0], D[0]):
        results.append({
            "text": chunks[idx]["text"],
            "source": chunks[idx]["source"],
            "page": chunks[idx]["page"],
            "score": float(score)
        })
    return results
