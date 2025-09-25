import fitz  # PyMuPDF
# src/ingest.py


def extract_pdf(path):
    """
    Reads a PDF and extracts text page by page.
    Returns a list of dictionaries: {'source', 'page', 'text'}
    """
    chunks = []
    doc = fitz.open(path)
    for page_no in range(len(doc)):
        text = doc.load_page(page_no).get_text("text")
        chunks.append({
            "source": path,
            "page": page_no+1,
            "text": text
        })
    return chunks
