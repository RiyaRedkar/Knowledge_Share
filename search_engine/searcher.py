# searcher.py

from search_engine.chroma_client import get_chroma_collection

# Ranking weights (LOCKED)
SEMANTIC_WEIGHT = 0.7
VERIFICATION_WEIGHT = 0.3

# Optional safety filter
MIN_VERIFICATION_SCORE = 40


def search_posts(user_query: str, top_k: int = 3):
    """
    Search for relevant posts using semantic similarity
    and re-rank using verification score.
    """
    collection = get_chroma_collection()

    # Query ChromaDB
    results = collection.query(
        query_texts=[user_query],
        n_results=5,   # retrieve more, rank later
        include=["metadatas", "distances"]
    )

    ranked_results = []

    # Chroma returns lists inside lists
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for metadata, distance in zip(metadatas, distances):
        verification_score = metadata.get("verification_score", 0)

        # Filter low-trust content
        if verification_score < MIN_VERIFICATION_SCORE:
            continue

        # Convert distance to similarity (Chroma uses distance)
        semantic_score = 1 / (1 + distance)

        verification_norm = verification_score / 100

        final_score = (
            SEMANTIC_WEIGHT * semantic_score
            + VERIFICATION_WEIGHT * verification_norm
        )

        ranked_results.append({
            "post_id": metadata.get("post_id"),
            "semantic_score": round(semantic_score, 4),
            "verification_score": verification_score,
            "final_score": round(final_score, 4)
        })

    # Sort by final score
    ranked_results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    return ranked_results[:top_k]
