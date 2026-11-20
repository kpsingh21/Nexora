from typing import List, TypedDict
import time

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama


from langgraph.graph import StateGraph, START, END
from dotenv import load_dotenv

load_dotenv()



docs = (
    PyPDFLoader("./Documents/book1.pdf").load() +
    PyPDFLoader("./Documents/book2.pdf").load() +
    PyPDFLoader("./Documents/book3.pdf").load()
)

# print(len(docs))

# 2) Chunk
chunks = RecursiveCharacterTextSplitter(chunk_size=900, chunk_overlap=150).split_documents(docs)

# 3) Clean text to avoid UnicodeEncodeError (surrogates from PDF extraction)
for d in chunks:
    d.page_content = d.page_content.encode("utf-8", "ignore").decode("utf-8", "ignore")

# print(len(chunks),"chunkslength") #6399
