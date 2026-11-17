# Lab 6: Building a Tool-Using AI Agent with Ollama

**Module:** PUSL 3205 - Large Language Models and Generative AI
**Tools:** Python 3.12, LangChain, Ollama (Llama 3.2 3B), SQLite, PyAutoGUI, ChromaDB, Google Calendar API

## Objective
In this lab I built an AI agent that can use tools. A normal chatbot only replies with text. My agent can also run small Python functions (tools): it opens the Windows Calculator, remembers things I tell it, searches a university handbook, and adds events to my Google Calendar.

## How the agent works
```
User question
     |
     v
Llama 3.2 decides: answer directly, or use a tool?
     |-- tool --> the Python function runs --> the result goes back to the model
     |
     v
Final answer
```
The model is given a list of tools and a short description of each one. If it decides a tool is needed, my code runs that function and gives the result back to the model, which then writes the answer. This repeats until the model answers without a tool. The loop is in `agent_core.py`.

## Setup
| Item | Value |
|------|-------|
| Python | 3.12, virtual environment `agent_env` |
| LLM | Llama 3.2 3B via Ollama (`llama3.2:3b`) |
| Embedding model (Part C) | Qwen3 Embedding 0.6B |
| Libraries | langchain, langchain-ollama, pyautogui, pygetwindow, langchain-community, langchain-chroma, chromadb, pymupdf |

## Files
| File | What it does |
|------|--------------|
| `tools.py` | The tools: calculator, date/time, Notepad, file search, file creation, system information |
| `agent_core.py` | The agent loop (call model, run tools, repeat) |
| `part_a_calculator.py` | Part A: calculator agent |
| `part_a_multi_tools.py` | Part A exercise: agent with six tools |
| `memory.py` | SQLite memory (save statements, search them) |
| `part_b_memory_agent.py` | Part B: calculator + memory search tool |
| `part_c_rag_agent.py` | Part C: calculator + memory search + RAG search |
| `ingest.py`, `rag_pipeline.py` | Reused from Lab 5 to build and query the handbook database |
| `google_calendar_tools.py` | Google Calendar tools: create an event, check today's schedule |
| `part_d_calendar_agent.py` | Part D: agent with the Google Calendar tools |

## Part A: Calculator agent
The calculator tool checks the sum with Python and then opens Windows Calculator and types it with PyAutoGUI, so the calculation can be watched.

Test: `Calculate 25 x 4` -> the agent called `calculator({'expression': '25 * 4'})`, Calculator opened and showed **100**, and the agent answered "The result of 25 x 4 is 100".

### Exercise: six tools
| # | Query | Tool used | Result |
|---|-------|-----------|--------|
| 1 | Calculate 25 × 4 | `calculator` | Correct (100) |
| 2 | What is the date today? | `get_date_time` | Correct (17 November 2026) |
| 3 | Open Notepad and write Hello Students | `open_notepad` | Notepad opened with the text |
| 4 | Find all PDF files in D:\MSC AI | `file_search` | The folder does not exist on this computer; the tool said so and the agent explained it |
| 4b | Find all PDF files in my Desktop folder | `file_search` | The search ran correctly and found no PDFs there |
| 5 | Create a file called test.txt ... with Hello World | `create_file` | The tool reported the file was created |
| 6 | Show my computer specifications | `system_info` | Windows 11, 16 CPU cores, 15.6 GB RAM |

## Part B: Memory with SQLite
Every statement the user makes is saved in a SQLite file (`agent_memory.db`); questions are not saved. The `memory_search` tool looks for stored statements that share a keyword with the query.

| | Without memory | With memory |
|---|---|---|
| "My name is Alex." | Greeted the user | Greeted the user and saved the statement |
| "What is my name?" | "I don't have any information about your name" | Called `memory_search`, found "My name is Alex", answered "Your name is Alex" |
| After restarting the program | not applicable | Still answered "Your name is Alex", because the memory is stored in the database file |

## Part C: RAG-powered agent
The agent has three tools: `calculator`, `memory_search` and `rag_search`. The RAG tool searches the NSBM computing awards handbook, using the ChromaDB database from Lab 5 (39 chunks).

| Question | Tool chosen | Agent answer | Correct? |
|----------|-------------|--------------|----------|
| How many credits is Advanced Mathematics for Computing? | `rag_search` | 3 credits | Yes |
| What is the aim of the BSc Honours in Computer Science programme? | `rag_search` | To produce competent, well-moulded computer professionals with a sound technical foundation | Yes |
| Calculate 25 x 4 | `calculator` | 100 | Yes |
| What is my name? | `memory_search` | Alex | Yes |

## What I observed
- **Clear requests went to the right tool.** Every question in the tables above used the correct tool without me naming it.
- **The small 3B model sometimes chose the wrong tool.** When no memory tool was available, "what is my name?" was sent to the calculator. Pasting a command like `python part_b_memory_agent.py` into the prompt made it call `system_info`. And "My name is Alex." made it run a sum that it copied from my calculator description.
- **Tool descriptions matter.** The calculator description had an example sum, and the model copied it. I removed the example and told the model to use the calculator only for real calculations, and the problem stopped.
- **Memory made a real difference.** Without it the agent could not answer questions about what I had said earlier. With the SQLite file it still knew my name after I restarted the program.
- **Vague input gave a confused answer.** I typed a sentence that was not a real question, and the agent still searched the handbook and gave a muddled answer instead of saying it did not understand.
- **Retrieval can pick the wrong programme.** The handbook has similar pages for several programmes, and one search returned text from Computer Networks instead of Computer Science.
- **Approval protects the calendar.** The calendar tool asks me to type `y` before it creates an event, so a wrong guess by the model cannot change my calendar by itself.

## Limitations
- The model is small, so its choice of tool and its arguments cannot be fully trusted.
- The memory search only matches keywords, so it can miss a fact if I ask using different words.
- The Calculator, Notepad and system-information tools only work on Windows. PyAutoGUI types into the front window, so I must not touch the mouse or keyboard while it runs.
- The file tools can read and write files on the computer, so a real system would need permission checks.

## Part D: Google Calendar tools
I added two tools: `get_todays_schedule` and `create_calendar_event`. They use the Google Calendar API. To set this up I created a Google Cloud project, enabled the Calendar API, made an OAuth client (Desktop app) and added my own account as a test user. The first run opens a browser to sign in, and the permission is saved in `token.json`. The agent is told today's date in its system prompt, so it can turn "tomorrow" into a real date. Before an event is created I have to type `y` to approve it.

| Request | Tool called | Result |
|---------|-------------|--------|
| What is on my calendar today? | `get_todays_schedule` | "No events today" |
| Add a meeting called Lab review tomorrow at 3 pm for 30 minutes | `create_calendar_event` (2026-11-18, 15:00, 30 minutes) | After I typed `y`, the event appeared in Google Calendar on 18 November at 3 PM |

Problems I fixed during setup: `credentials.json` was not in the folder; Google blocked the sign-in (Error 403: access_denied) until I added my account as a test user; and the Calendar API had to be enabled in the project. None of these were code errors. `credentials.json` and `token.json` give access to my Google account, so they are in `.gitignore` and are not uploaded.

## Part E: n8n
Not part of this submission: the lecturer asked for Parts A to D only.

## How to run
```
py -3.12 -m venv agent_env
agent_env\Scripts\activate.bat
python -m pip install langchain langchain-ollama pyautogui pygetwindow langchain-community langchain-chroma chromadb pymupdf google-api-python-client google-auth-oauthlib google-auth-httplib2
ollama pull llama3.2:3b
ollama pull qwen3-embedding:0.6b
python part_a_calculator.py
python part_a_multi_tools.py
python part_b_memory_agent.py          (add "nomemory" to compare, "clear" to empty the memory)
python ingest.py                        (put the handbook PDF in data/ first)
python part_c_rag_agent.py
python part_d_calendar_agent.py         (needs your own credentials.json from Google Cloud)
```

## Folder contents
```
lab-06-tool-using-agent/
├── README.md
├── tools.py  agent_core.py  memory.py
├── part_a_calculator.py  part_a_multi_tools.py
├── part_b_memory_agent.py  part_c_rag_agent.py
├── google_calendar_tools.py  part_d_calendar_agent.py
├── ingest.py  rag_pipeline.py
├── .gitignore
├── data/            (the handbook PDF)
└── screenshots/
```
`agent_env/`, `chroma_db/`, `agent_memory.db`, `credentials.json` and `token.json` are not uploaded (see `.gitignore`).
