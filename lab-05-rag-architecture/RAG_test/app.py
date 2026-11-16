"""Streamlit chat window for the university RAG assistant."""
import os
import streamlit as st
from ingest import ingest_pdf, DATA_DIR
from rag_pipeline import get_vectorstore, ask, list_sources

st.set_page_config(page_title="University Knowledge Assistant", page_icon="🎓")
st.title("🎓 University Knowledge Assistant")

os.makedirs(DATA_DIR, exist_ok=True)
vectorstore = get_vectorstore()

# ---- Sidebar: upload your own PDFs ----
with st.sidebar:
    st.header("Documents")
    uploaded = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
    if uploaded and st.button("Add to knowledge base"):
        for f in uploaded:
            path = os.path.join(DATA_DIR, f.name)
            with open(path, "wb") as out:
                out.write(f.getbuffer())
            with st.spinner(f"Reading {f.name}..."):
                n = ingest_pdf(path, vectorstore)
            st.success(f"{f.name}: {n} chunks added")
    st.subheader("Documents in the database")
    sources = list_sources(vectorstore)
    if sources:
        for s in sources:
            st.write("•", s)
    else:
        st.write("None yet. Upload a PDF above.")

# ---- Chat ----
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

question = st.chat_input("Ask a university question")
if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            answer, docs = ask(question, vectorstore=vectorstore)
        st.markdown(answer)
        if docs:
            with st.expander("Sources"):
                for d in docs:
                    st.markdown(f"**{d.metadata.get('source')}**, page {d.metadata.get('page', 0) + 1}")
                    st.caption(d.page_content[:300] + "...")
    st.session_state.messages.append({"role": "assistant", "content": answer})
