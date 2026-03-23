import json
from embeddings import get_embedding
from vector_store import VectorStore
from config import DATA_PATH, INDEX_PATH

with open(DATA_PATH, 'r') as f:
    faqs = json.load(f)

print("Building index...")

vectors = [get_embedding(faq['question']) for faq in faqs]

vector_store = VectorStore(dim=len(vectors[0]))
vector_store.add(vectors)
vector_store.save(INDEX_PATH)

print(f"Index built and saved! Total FAQs indexed: {len(faqs)}")
