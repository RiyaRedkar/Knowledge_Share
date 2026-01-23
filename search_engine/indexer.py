# indexer.py

from search_engine.embeddings import embed
from search_engine.search_document import build_search_document
from search_engine.chroma_client import get_chroma_collection

collection = get_chroma_collection()

def index_post(post: dict):
    search_text = build_search_document(post)
    vector = embed(search_text)

    collection.add(
        ids=[post["post_id"]],
        documents=[search_text],
        embeddings=[vector],
        metadatas=[{
            "post_id": post["post_id"],
            "verification_score": post["validation_score"],
            "region": post.get("region", "")
        }]
    )
