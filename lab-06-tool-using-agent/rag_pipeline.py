"""RAG pipeline: retrieve chunks from ChromaDB and answer with Llama 3.2 via Ollama."""
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, ChatOllama

CHROMA_DIR = "chroma_db"
COLLECTION = "university_docs"
EMBED_MODEL = "qwen3-embedding:0.6b"
LLM_MODEL = "llama3.2:3b"
TOP_K = 6

PROMPT = """You are a university knowledge assistant.
Answer the question using the context below.
- Use only information from the context. Do not make things up.
- If the context only partly answers the question, give what it does say and mention what is missing.
- If the context has nothing relevant, say: "I could not find this in the provided documents."

Context:
{context}

Question: {question}

Answer:"""


def get_vectorstore():
    embeddings = OllamaEmbeddings(model=EMBED_MODEL)
    return Chroma(
        collection_name=COLLECTION,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )


def list_sources(vectorstore=None):
    """Return the names of the PDFs that are already in the database."""
    vectorstore = vectorstore or get_vectorstore()
    data = vectorstore.get(include=["metadatas"])
    return sorted({m.get("source", "unknown") for m in data["metadatas"]})


def ask(question, k=TOP_K, vectorstore=None):
    """Return (answer, list of source chunks)."""
    vectorstore = vectorstore or get_vectorstore()
    docs = vectorstore.similarity_search(question, k=k)
    if not docs:
        return "No documents have been added yet. Run ingest.py or upload a PDF first.", []
    context = "\n\n".join(
        f"[{d.metadata.get('source')} - page {d.metadata.get('page', 0) + 1}]\n{d.page_content}"
        for d in docs
    )
    llm = ChatOllama(model=LLM_MODEL, temperature=0)
    answer = llm.invoke(PROMPT.format(context=context, question=question)).content
    return answer, docs


if __name__ == "__main__":
    vs = get_vectorstore()
    while True:
        q = input("\nAsk a university question (or exit): ").strip()
        if q.lower() in ("exit", "quit", ""):
            break
        answer, docs = ask(q, vectorstore=vs)
        print("\nAnswer:", answer)
        print("\nSources:")
        for d in docs:
            print(f"  - {d.metadata.get('source')} (page {d.metadata.get('page', 0) + 1})")
