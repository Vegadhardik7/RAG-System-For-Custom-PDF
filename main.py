# rag_app.py

import os
import streamlit as st
import logging
from dotenv import load_dotenv
from PyPDF2 import PdfReader

from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Cassandra
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pydantic import SecretStr
import cassio

# Load environment variables
load_dotenv()

# Streamlit App Title
st.title("📜 Ask Your PDF (RAG with Gemini + Astra DB)")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

# Setup inputs and session state
if uploaded_file and "rag_chain" not in st.session_state:

    st.success("📄 PDF uploaded! Processing...")

    # Read and extract text
    pdf = PdfReader(uploaded_file)
    raw_text = ""
    for page in pdf.pages:
        content = page.extract_text()
        if content:
            raw_text += content

    # Load environment vars
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
    ASTRA_DB_ID = os.getenv("ASTRA_DB_ID")
    ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")  # <-- Required!

    # Check for missing variables and report which ones are missing
    required_vars = {
        "GOOGLE_API_KEY": GOOGLE_API_KEY,
        "ASTRA_DB_APPLICATION_TOKEN": ASTRA_DB_APPLICATION_TOKEN,
        "ASTRA_DB_ID": ASTRA_DB_ID,
        "ASTRA_DB_KEYSPACE": ASTRA_DB_KEYSPACE,
    }
    missing_vars = [name for name, value in required_vars.items() if not value]
    if missing_vars:
        st.error(f"❌ Please check your .env file for missing variables: {', '.join(missing_vars)}")
        st.stop()

    # Init Cassandra (Astra DB)
    cassio.init(token=ASTRA_DB_APPLICATION_TOKEN, database_id=ASTRA_DB_ID, keyspace=ASTRA_DB_KEYSPACE)

    # LLM and Embeddings
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash-latest",
        temperature=0.6,
        convert_system_message_to_human=True
    )

    embedding = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key=SecretStr(GOOGLE_API_KEY) if GOOGLE_API_KEY else None
    )

    # Vector Store
    vector_store = Cassandra(
        embedding=embedding,
        table_name="qa_streamlit_demo",  # change as needed
    )

    # Split and insert text
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_text(raw_text)
    vector_store.add_texts(chunks)

    # Create retriever
    retriever = vector_store.as_retriever()

    # Prompt + RAG Chain
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful AI assistant. Answer the user's question based *only* on the provided context.\nContext: {context}"),
        ("human", "{input}")
    ])
    doc_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, doc_chain)

    # Store in session
    st.session_state["rag_chain"] = retrieval_chain
    st.success("✅ PDF indexed! You can now ask questions.")

# Ask Questions
if "rag_chain" in st.session_state:
    query = st.text_input("💬 Ask a question about the PDF:")

    if query:
        with st.spinner("🤖 Thinking..."):
            try:
                result = st.session_state["rag_chain"].invoke({"input": query})
                st.markdown(f"**Answer:** {result['answer']}")
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
