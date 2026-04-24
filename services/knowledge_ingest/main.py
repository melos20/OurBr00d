import os
import time
import chromadb
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import SentenceTransformerEmbeddings

CHROMA_URL = os.getenv("CHROMA_URL", "http://chroma:8000")
KNOWLEDGE_DIR = os.getenv("KNOWLEDGE_DIR", "/knowledge")

def ingest():
    print(f"Scanning {KNOWLEDGE_DIR} for new knowledge...")
    
    # 1. Load Documents
    pdf_loader = DirectoryLoader(KNOWLEDGE_DIR, glob="./*.pdf", loader_cls=PyPDFLoader)
    txt_loader = DirectoryLoader(KNOWLEDGE_DIR, glob="./*.txt", loader_cls=TextLoader)
    
    docs = pdf_loader.load() + txt_loader.load()
    if not docs:
        print("No documents found.")
        return

    # 2. Split into Chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    # 3. Embed and Store in Chroma
    client = chromadb.HttpClient(host="chroma", port=8000)
    collection = client.get_or_create_collection(name="parenting_knowledge")
    
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    for i, split in enumerate(splits):
        collection.upsert(
            ids=[f"doc_{i}"],
            documents=[split.page_content],
            metadatas=[split.metadata]
        )
    
    print(f"Successfully ingested {len(splits)} chunks into ChromaDB.")

if __name__ == "__main__":
    # Initial ingest
    time.sleep(10) # Wait for Chroma to start
    ingest()
    
    # In a real setup, we'd use watchdog here. For MVP, we just exit or sleep.
    while True:
        time.sleep(3600)
