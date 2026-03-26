from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import streamlit as st
import os

load_dotenv(dotenv_path="env")


api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("API key not found!")
    st.stop()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.9,
    google_api_key=api_key
)

prompt = PromptTemplate(
    input_variables=["history", "question"],
    template="""You are a helpful assistant.

Conversation history:
{history}

User: {question}
Assistant:"""
)

chain = prompt | llm

st.title("💬 LangChain Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask me anything:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    history = "\n".join([
        f"{m['role'].capitalize()}: {m['content']}"
        for m in st.session_state.messages[:-1]
    ])

    response = chain.invoke({"history": history, "question": user_input})
    reply = response.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
