"""Ingestion: read PDFs, split into chunks, embed them and store them in ChromaDB."""
import os
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag_pipeline import get_vectorstore

DATA_DIR = "data"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150


def ingest_pdf(path, vectorstore=None):
    """Add one PDF to the database. Returns the number of chunks added."""
    vectorstore = vectorstore or get_vectorstore()
    name = os.path.basename(path)

    pages = PyMuPDFLoader(path).load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(pages)

    for c in chunks:
        c.metadata["source"] = name

    # Fixed ids mean running ingest twice on the same file does not create duplicates.
    ids = [f"{name}-{i}" for i in range(len(chunks))]
    vectorstore.add_documents(chunks, ids=ids)
    return len(chunks)


def ingest_folder(folder=DATA_DIR):
    vectorstore = get_vectorstore()
    pdfs = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
    if not pdfs:
        print(f"No PDF files found in '{folder}'. Put your PDFs there first.")
        return
    for f in pdfs:
        n = ingest_pdf(os.path.join(folder, f), vectorstore)
        print(f"{f}: {n} chunks stored")
    print("Done.")


if __name__ == "__main__":
    ingest_folder()
