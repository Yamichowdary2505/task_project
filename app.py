from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from llm import GeminiLLM
import streamlit as st

st.set_page_config(page_title="LangChain Chatbot", layout="wide")
st.title("💬 Chatbot")

llm = GeminiLLM()

# ── Text Splitter Section ──
st.sidebar.title(" Load Document")
uploaded_file = st.sidebar.file_uploader("Upload a .txt file", type=["txt"])

doc_context = ""

if uploaded_file:
    with open("temp.txt", "wb") as f:
        f.write(uploaded_file.read())

    loader = TextLoader("temp.txt")
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0
    )
    docs = text_splitter.split_documents(documents)

    doc_context = "\n".join([doc.page_content for doc in docs])
    st.sidebar.success(f"Loaded! Split into {len(docs)} chunks ")

# ── Prompt Template ──
prompt = PromptTemplate(
    input_variables=["context", "history", "question"],
    template="""You are a helpful assistant.

Document context (if any):
{context}

Conversation history:
{history}

User: {question}
Assistant:"""
)

chain = prompt | llm

# ── Chat UI ──
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

    response = chain.invoke({
        "context": doc_context,
        "history": history,
        "question": user_input
    })

    reply = response if isinstance(response, str) else response.content

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)