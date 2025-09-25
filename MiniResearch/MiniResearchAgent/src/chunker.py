def chunk_text(text, chunk_size=500, overlap=100):
    """
    Splits text into smaller pieces for better searching.
    chunk_size: number of characters per chunk
    overlap: number of characters to overlap between chunks
    """
    if not text:
        return []

    chunks = []
    start = 0
    # step is how much we advance each iteration; ensure it's positive
    step = chunk_size - overlap
    if step <= 0:
        # overlap too large; fall back to non-overlapping chunks
        step = chunk_size

    text_len = len(text)
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunks.append(text[start:end])
        start += step

    return chunks
