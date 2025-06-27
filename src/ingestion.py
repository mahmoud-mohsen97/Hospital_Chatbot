import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_openai import OpenAIEmbeddings
from config.settings import KNOWLEDGE_BASE_FILE

load_dotenv()

# Use the specified CSV file path
csv_file = str(KNOWLEDGE_BASE_FILE)

if not os.path.exists(csv_file):
    raise FileNotFoundError(f"CSV file '{csv_file}' not found. Please ensure it exists.")

loader = CSVLoader(file_path=csv_file)
doc_splits = loader.load_and_split()

print(f"Loaded {len(doc_splits)} documents from {csv_file}")

# Create the chroma directory if it doesn't exist
chroma_dir = "./.chroma"
os.makedirs(chroma_dir, exist_ok=True)

# Try to initialize ChromaDB, fall back to in-memory if file permissions fail
try:
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=OpenAIEmbeddings(model="text-embedding-3-large"),
        persist_directory=chroma_dir,
    )
    print(f"ChromaDB initialized with persistent storage at {chroma_dir}")
except Exception as e:
    print(f"Failed to initialize persistent ChromaDB: {e}")
    print("Falling back to in-memory ChromaDB...")
    vectorstore = Chroma.from_documents(
        documents=doc_splits,
        collection_name="rag-chroma",
        embedding=OpenAIEmbeddings(model="text-embedding-3-large"),
    )
    print("ChromaDB initialized in-memory mode")

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3},
    search_type="similarity",
)
