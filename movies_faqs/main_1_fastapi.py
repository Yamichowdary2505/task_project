from fastapi import FastAPI
from faq_service import get_faq_answer

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Movie FAQ API!"}

@app.post("/ask")
def ask(query: str):
    answer = get_faq_answer(query)
    return {"query": query, "answer": answer}