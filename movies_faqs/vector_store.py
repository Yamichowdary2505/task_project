import faiss
import numpy as np
import os

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatIP(dim)

    def add(self, vectors):
        self.index.add(np.array(vectors).astype('float32'))

    def search(self, query_vector, k=5):
        distances, indices = self.index.search(
            np.array([query_vector]).astype('float32'), k
        )
        return indices[0]

    def save(self, path):
        faiss.write_index(self.index, path)

    def load(self, path):
        if os.path.exists(path):
            self.index = faiss.read_index(path)
