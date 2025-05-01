import os
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from typing import List
from dotenv import load_dotenv

load_dotenv()  # Load your .env file with GOOGLE_API_KEY

def create_vector_store(text_chunks: List[str], index_path: str = "faiss_index"):
    """
    Creates and saves a FAISS vector store from text chunks using Gemini embeddings.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local(index_path)


def load_vector_store(index_path: str = "faiss_index"):
    """
    Loads an existing FAISS vector store.
    """
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.load_local(index_path, embeddings, allow_dangerous_deserialization=True)
    return vector_store
