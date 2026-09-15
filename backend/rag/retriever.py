from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_PATH = BASE_DIR / "chroma_db"


embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)


vector_db = Chroma(
    persist_directory=str(CHROMA_PATH),
    embedding_function=embeddings,
)


retriever = vector_db.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 4
    }
)