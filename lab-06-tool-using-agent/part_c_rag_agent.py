"""Part C: agent with three tools: calculator, memory search and RAG search (Lab 5 handbook database)."""
from langchain_core.tools import tool
from tools import calculator
from agent_core import build_agent, run_agent
from part_b_memory_agent import memory_search
import memory
from rag_pipeline import get_vectorstore

_vectorstore = None


@tool
def rag_search(question: str) -> str:
    """Search the university knowledge base (the NSBM computing awards handbook: programmes, modules,
    credits, core and elective subjects). Use this for any question about the university or its programmes."""
    global _vectorstore
    if _vectorstore is None:
        _vectorstore = get_vectorstore()
    docs = _vectorstore.similarity_search(question, k=4)
    if not docs:
        return "No documents found. Run ingest.py first."
    return "\n\n".join(f"[{d.metadata.get('source')} - page {d.metadata.get('page', 0) + 1}]\n{d.page_content}"
                       for d in docs)


def main():
    llm_with_tools, by_name = build_agent([calculator, memory_search, rag_search])
    print("Agent with calculator + memory + university RAG. Type exit to stop.")
    while True:
        q = input("\nYou (or exit): ").strip()
        if q.lower() in ("exit", "quit", ""):
            break
        print("Agent:", run_agent(llm_with_tools, by_name, q))
        if memory.save_memory(q):
            print("  [memory] saved")


if __name__ == "__main__":
    main()
