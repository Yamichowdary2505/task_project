import json
from embeddings import get_embedding
from config import DATA_PATH

with open(DATA_PATH, 'r') as f:
    faqs = json.load(f)

def retrieve(query, vector_store, top_k=3):
    query_vec = get_embedding(query)
    indices = vector_store.search(query_vec, k=top_k)
    results = [faqs[i] for i in indices]
    return results
