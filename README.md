## MiniResearchAgent

A minimal research assistant that ingests a PDF, chunks the text, embeds it, indexes vectors, and serves a simple Streamlit UI for retrieval-augmented Q&A.

### Project structure

```
MiniResearchAgent/
  app/
    streamlit_app.py        # Streamlit UI entrypoint
  data/
    hr.pdf                  # Sample document(s) to ingest
  requirements.txt          # Python dependencies
  src/
    __init__.py
    chunker.py              # Text chunking utilities
    embed.py                # Embedding routines
    index.py                # Vector index build/load helpers
    ingest.py               # End-to-end ingestion pipeline
    retrieve.py             # Retrieval utilities
```

### Prerequisites

- Python 3.10+ recommended
- On Windows PowerShell (this repo was tested on Windows 10/11)

### Setup

```powershell
# From the workspace root
cd MiniResearchAgent

# (Optional) Create and activate a virtual environment
python -m venv .venv
. .venv/Scripts/Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Run the Streamlit app

```powershell
streamlit run app/streamlit_app.py
```

Then open the URL shown in the terminal (typically `http://localhost:8501`).

### Ingest your documents

Place your PDFs in `data/`. The sample `data/hr.pdf` is included.

Run the ingestion pipeline (parsing → chunking → embedding → indexing):

```powershell
python -m src.ingest
```

If your pipeline expects specific environment variables (e.g., for hosted embedding models), set them before running. Otherwise, the default local/OSS models from `requirements.txt` will be used if available.

### Typical workflow

1. Add or update files in `data/`.
2. Run `python -m src.ingest` to rebuild the index.
3. Start the UI with `streamlit run app/streamlit_app.py`.
4. Ask questions; the app retrieves relevant chunks and composes an answer.

### Key modules overview

- `src/chunker.py`: Splits raw text into overlapping windows suitable for embedding.
- `src/embed.py`: Turns chunks into vector embeddings via the configured model.
- `src/index.py`: Builds and persists a vector index; provides load/save helpers.
- `src/ingest.py`: Orchestrates reading `data/`, chunking, embedding, and indexing.
- `src/retrieve.py`: Queries the index to fetch top-k relevant chunks.
- `app/streamlit_app.py`: Simple UI to type a query and view retrieved context/answers.

### Troubleshooting

- If `streamlit` command is not found, ensure the virtual environment is activated and `pip install -r requirements.txt` succeeded.
- If ingestion finds no files, verify your PDFs are in `MiniResearchAgent/data/`.
- On Windows, execution policy may block venv activation. You can run PowerShell as Administrator and execute:
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```

### License

This project is provided as-is for educational purposes.
