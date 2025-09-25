import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.ingest import extract_pdf
from src.chunker import chunk_text
from src.embed import get_embeddings
from src.index import build_faiss_index
from src.retrieve import retrieve
import faiss
import gc


st.title("Mini Research Agent (Local PDFs)")

# UI: choose a PDF (default to bundled one)
pdf_path = st.text_input("PDF path:", value="data/hr.pdf")

# Controls: batch size is chosen automatically based on document size


if 'index' not in st.session_state:
    st.session_state['index'] = None
if 'chunks' not in st.session_state:
    st.session_state['chunks'] = []


def build_index_from_pdf(path: str, batch_size: int = 64):
    """
    Build FAISS index incrementally in batches to reduce peak memory.
    Stores index and chunks metadata in session_state.
    """
    st.session_state['index'] = None
    st.session_state['chunks'] = []
    buffer_texts = []
    buffer_meta = []

    pages = extract_pdf(path)
    progress = st.progress(0)
    total_pages = len(pages)
    processed = 0

    # estimate total chunks so we can pick an automatic batch size if caller passed None
    if batch_size is None:
        est_chunks = 0
        for p in pages:
            est_chunks += max(1, len(list(chunk_text(p['text']))))
        # pick a batch size scaled to document size: aim for ~20 batches
        est = max(16, min(256, est_chunks // 20 if est_chunks >= 20 else 64))
        batch_size = est

    for page in pages:
        for ch in chunk_text(page['text']):
            buffer_texts.append(ch)
            buffer_meta.append({"text": ch, "source": page['source'], "page": page['page']})

            if len(buffer_texts) >= batch_size:
                embs = get_embeddings(buffer_texts)
                if st.session_state['index'] is None:
                    st.session_state['index'] = build_faiss_index(embs)
                else:
                    st.session_state['index'].add(embs)

                # append metadata and clear buffers
                st.session_state['chunks'].extend(buffer_meta)
                buffer_texts = []
                buffer_meta = []
                gc.collect()

        processed += 1
        progress.progress(int(processed / total_pages * 100))

    # final batch
    if buffer_texts:
        embs = get_embeddings(buffer_texts)
        if st.session_state['index'] is None:
            st.session_state['index'] = build_faiss_index(embs)
        else:
            st.session_state['index'].add(embs)
        st.session_state['chunks'].extend(buffer_meta)
        gc.collect()


if st.button("Build index"):
    with st.spinner("Building index, this can take a while on first run..."):
        # pass None so the function will auto-select a batch size
        build_index_from_pdf(pdf_path, None)
    st.success(f"Index built. {len(st.session_state['chunks'])} chunks indexed.")

query = st.text_input("Ask a question:")
k = st.slider("Number of chunks to retrieve:", 1, 10, 5)

if st.button("Search"):
    if st.session_state.get('index') is None or len(st.session_state.get('chunks', [])) == 0:
        st.warning("Index is empty — click 'Build index' first.")
    else:
        results = retrieve(query, st.session_state['index'], st.session_state['chunks'], k)
        st.subheader("Top results:")
        for r in results:
            st.markdown(f"**Source:** {r['source']} | **Page:** {r['page']} | **Score:** {r['score']:.2f}")
            st.write(r['text'])
