# chroma_client.py

import os
import chromadb

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_PATH = os.path.join(BASE_DIR, "chroma_store")

_client = None
_collection = None

def get_chroma_collection():
    global _client, _collection

    if _collection is None:
        _client = chromadb.PersistentClient(path=CHROMA_PATH)

        _collection = _client.get_or_create_collection(
            name="knowledge_posts"
        )

    return _collection
