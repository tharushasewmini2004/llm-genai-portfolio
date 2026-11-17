"""Part B: an agent with a calculator and a SQLite memory search tool.

python part_b_memory_agent.py            -> agent WITH memory
python part_b_memory_agent.py nomemory   -> same agent WITHOUT memory (for comparison)
python part_b_memory_agent.py clear      -> empty the memory database
"""
import sys
from langchain_core.tools import tool
from tools import calculator
from agent_core import build_agent, run_agent
import memory


@tool
def memory_search(query: str) -> str:
    """Search the user's stored personal information (name, preferences, facts they told you earlier).
    Use this whenever the user asks about something they told you before."""
    rows = memory.search_memory(query)
    if not rows:
        return "No stored information found."
    return "Stored information:\n" + "\n".join(f"- {content} (told on {created})" for content, created in rows)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "memory"
    if mode == "clear":
        memory.clear_memory()
        print("Memory cleared.")
        return
    use_memory = mode != "nomemory"
    tools = [calculator, memory_search] if use_memory else [calculator]
    llm_with_tools, by_name = build_agent(tools)
    print("Agent WITH memory" if use_memory else "Agent WITHOUT memory",
          "- try: My name is Alex.  then: What is my name?")
    while True:
        q = input("\nYou (or exit): ").strip()
        if q.lower() in ("exit", "quit", ""):
            break
        print("Agent:", run_agent(llm_with_tools, by_name, q))
        if use_memory and memory.save_memory(q):   # save AFTER answering so a question never finds itself
            print("  [memory] saved")


if __name__ == "__main__":
    main()
