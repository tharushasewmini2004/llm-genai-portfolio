# Lab 5: RAG Architecture - University Knowledge Assistant

**Module:** PUSL 3205 - Large Language Models and Generative AI
**Tools:** Python 3.12, LangChain, ChromaDB, Ollama, Streamlit, PyMuPDF

## Objective
Build a Retrieval-Augmented Generation (RAG) application that answers questions from university PDF documents, then extend it so it can read more PDFs and let users upload their own.

## What RAG does
A language model on its own does not know the contents of my university documents. RAG fixes this in two steps:
1. **Retrieve:** the question is turned into an embedding and the most similar chunks of the documents are found in a vector database.
2. **Generate:** those chunks are given to the LLM together with the question, and it answers from them.

```
PDFs -> split into chunks -> embeddings -> ChromaDB
                                             |
Question -> embedding -> top 6 similar chunks -> prompt -> Llama 3.2 -> answer + sources
```

## Setup
| Item | Value |
|------|-------|
| Python | 3.12.7 in a virtual environment (`rag_env`) |
| LLM | Llama 3.2 3B via Ollama |
| Embedding model | Qwen3 Embedding 0.6B via Ollama |
| Vector database | ChromaDB (saved in `chroma_db/`) |
| Framework | LangChain |
| Chat interface | Streamlit |
| Libraries | listed in `requirements.txt` |

Steps: create the virtual environment, install the libraries, run `ollama pull llama3.2:3b` and `ollama pull qwen3-embedding:0.6b`, then check both with `ollama list`.

## Files
| File | What it does |
|------|--------------|
| `ingest.py` | Reads every PDF in `data/`, splits it into chunks of 1000 characters (150 overlap), embeds them and stores them in ChromaDB. Each chunk has a fixed id, so running it twice does not create duplicates. |
| `rag_pipeline.py` | Retrieves the 6 most similar chunks, builds a prompt and asks Llama 3.2. Prints the answer and the source pages. |
| `app.py` | Streamlit chat window with a sidebar to upload PDFs. |
| `requirements.txt` | Saved dependencies. |

## Ingestion results
| Document | Chunks stored |
|----------|---------------|
| COMPUTING AWARD HANDBOOK (NSBM) | 39 |
| Lab sheet 5 | 8 (added by mistake at first, later removed) |
| Uni handbook (uploaded through the chat window) | 12 |

## Task: read more PDFs and allow uploads
- `ingest.py` loops over **all** PDFs in `data/`, so adding more files to the folder and running it again adds them to the database.
- `app.py` has an **Upload PDFs** button in the sidebar. The file is saved to `data/`, split, embedded and added to ChromaDB straight away, with no restart. A message shows how many chunks were added, and the sidebar lists every document in the database.
- Every answer shows its sources (file name and page), so the user can check where the answer came from.

Test: I uploaded `Uni handbook.pdf` while the app was running. The app reported **12 chunks added** and the file appeared in the "Documents in the database" list.

Result of a question about the uploaded file: *(write one line here: what you asked and what the app answered)*

## Test results (terminal and chat)
| Question | Answer | Correct? |
|----------|--------|----------|
| How many credits is Advanced Mathematics for Computing? | 3 credits (MA301.3) | Yes, matches the handbook |
| What is the aim of the BSc Honours in Computer Science programme? | To produce competent, well-moulded computer professionals with a sound technical foundation | Yes, matches the handbook wording |
| What are the main subjects in the computer science degree program? | Listed 7 Year 3 modules with codes, all labelled "core" | Partly: the modules exist, but 3 of them (CN302.3, SE308.3, CS302.3) are electives |
| Which modules are electives in the computer science programme? | Listed 10 modules | Partly: only 3 of the 10 are Computer Science electives; the rest were core modules or modules from other programmes |

Screenshots are in the `screenshots/` folder.

## Key observations
- **Retrieval works for direct facts.** Questions with a single clear answer (credit value, programme aim) were answered correctly, and the sources pointed to the right pages.
- **The model uses real content.** Module names and codes in the answers come from the handbook, not from the model's own knowledge. The answers are different from what the base model said about unrelated lab questions in earlier labs.
- **Table questions were unreliable.** The handbook has a similar table for each programme (Computer Science, Software Engineering, IT and so on). Fixed-size chunking cuts these tables apart, so the retrieved chunks mix different programmes and the small 3B model attached the wrong "Core"/"Elective" label or the wrong programme. Asking two similar questions gave different labels for the same module.
- **Mixed documents contaminate answers.** When Lab sheet 5 was in the database, its chunks appeared in the sources for handbook questions. Removing it and rebuilding the database fixed this.
- **The prompt matters.** My first prompt told the model to say "I could not find this" unless the answer was complete, and it refused a question the handbook only partly answers. I loosened it to allow partial answers and raised the retrieved chunks from 4 to 6.

## Limitations
- Fixed-size chunks split tables and sections, which hurts questions about lists and categories.
- Plain similarity search returns only the top 6 chunks, so long lists are cut off.
- A 3B model can mix up details even when the right text is retrieved. The answers should be checked against the cited pages.
- Only text PDFs are supported; scanned PDFs would need OCR.
- Everything runs locally, so answers can take from several seconds to about a minute.

## Possible improvements
Section-based or parent-child chunking, hybrid search (keyword + vector), reranking, and a larger model would help with the table and list problems.

## How to run
```
py -3.12 -m venv rag_env
rag_env\Scripts\activate.bat
pip install -r requirements.txt
ollama pull llama3.2:3b
ollama pull qwen3-embedding:0.6b
python ingest.py            # put your PDFs in the data/ folder first
python rag_pipeline.py      # chat in the terminal
streamlit run app.py        # chat window with PDF upload
```

## Folder contents
```
lab-05-rag-architecture/
├── README.md
├── app.py
├── ingest.py
├── rag_pipeline.py
├── requirements.txt
├── .gitignore
├── data/            (the PDFs)
└── screenshots/
```
`rag_env/` and `chroma_db/` are not uploaded (see `.gitignore`); they are rebuilt with the commands above.
