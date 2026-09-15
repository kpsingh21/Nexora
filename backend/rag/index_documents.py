from pathlib import Path
from langchain_community.document_loaders import Docx2txtLoader
from langchain_text_splitters import  RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma


BASE_DIR = Path(__file__).resolve().parent
file_path = BASE_DIR / "Documents" / "corephp.docx"
chroma_path = BASE_DIR / "chroma_db"


# load document
loader = Docx2txtLoader(str(file_path))
documents = loader.load()
# print(documents)


#split doc in chunks 
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)
# print(chunks[1])


# embedding model
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# print(embeddings,"embeddings")

# Create and persist your Vector Database locally
vector_db = Chroma.from_documents(chunks, embeddings, persist_directory="./chroma_db")
# print(vector_db,"vector_db")


print(f"Indexed {len(chunks)} chunks")
print(f"Vector DB: {chroma_path}")
# retriever = vector_db.as_retriever(search_type="similarity", search_kwargs={"k": 4})

