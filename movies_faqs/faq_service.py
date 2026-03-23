import json
from embeddings import get_embedding
from vector_store import VectorStore
from retrieval import retrieve
from config import DATA_PATH, INDEX_PATH

with open(DATA_PATH, 'r') as f:
    faqs = json.load(f)

sample_vec = get_embedding("test")
vector_store = VectorStore(dim=len(sample_vec))
vector_store.load(INDEX_PATH)

def get_faq_answer(query: str):
    results = retrieve(query, vector_store)
    return results[0]['answer'] if results else "No answer found."
