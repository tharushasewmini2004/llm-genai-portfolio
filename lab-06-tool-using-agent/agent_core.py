"""A small tool-calling agent loop for Ollama (Llama 3.2 3B)."""
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

MODEL = "llama3.2:3b"
SYSTEM = ("You are a helpful assistant with tools. Use a tool only when the user's request clearly needs it. "
          "If the user is just chatting or telling you something about themselves, reply normally without a tool. "
          "Never use the calculator unless the user asks to calculate numbers. "
          "After a tool returns, answer the user briefly using its result.")


def build_agent(tools):
    llm = ChatOllama(model=MODEL, temperature=0)
    return llm.bind_tools(tools), {t.name: t for t in tools}


def run_agent(llm_with_tools, tools_by_name, question, history=None, max_steps=5, system=None):
    """Send the question, run any tools the model asks for, and return the final answer."""
    messages = [SystemMessage(content=system or SYSTEM)] + (history or []) + [HumanMessage(content=question)]
    for _ in range(max_steps):
        reply = llm_with_tools.invoke(messages)
        messages.append(reply)
        if not reply.tool_calls:          # no tool needed: this is the final answer
            return reply.content
        for call in reply.tool_calls:     # run every tool the model asked for
            print(f"  [tool] {call['name']}({call['args']})")
            try:
                result = tools_by_name[call["name"]].invoke(call["args"])
            except Exception as e:
                result = f"Tool error: {e}"
            shown = str(result).replace("\n", " ")
            print(f"  [result] {shown[:300]}{'...' if len(shown) > 300 else ''}")
            messages.append(ToolMessage(content=str(result), tool_call_id=call["id"]))
    return "Stopped: too many tool steps."


def chat_loop(tools):
    llm_with_tools, by_name = build_agent(tools)
    while True:
        q = input("\nYou (or exit): ").strip()
        if q.lower() in ("exit", "quit", ""):
            break
        print("Agent:", run_agent(llm_with_tools, by_name, q))
