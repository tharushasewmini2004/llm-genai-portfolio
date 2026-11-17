"""Part A: calculator agent. The Calculator opens and performs the calculation by itself."""
from tools import calculator
from agent_core import chat_loop

if __name__ == "__main__":
    print("Calculator agent. Try: Calculate 25 x 4")
    chat_loop([calculator])
