"""Part A exercise: the agent with six tools."""
from tools import calculator, get_date_time, open_notepad, file_search, create_file, system_info
from agent_core import chat_loop

if __name__ == "__main__":
    print("Multi-tool agent. Tools: calculator, date/time, notepad, file search, file creation, system info")
    chat_loop([calculator, get_date_time, open_notepad, file_search, create_file, system_info])
