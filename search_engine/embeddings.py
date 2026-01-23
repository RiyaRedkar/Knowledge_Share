# embeddings.py

from sentence_transformers import SentenceTransformer

# Load once
_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed(text: str) -> list[float]:
    """
    Convert text into embedding vector.
    """
    return _model.encode(text).tolist()
