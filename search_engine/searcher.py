from search_engine.chroma_client import get_chroma_collection

SEMANTIC_WEIGHT = 0.7
VERIFICATION_WEIGHT = 0.3
MIN_VERIFICATION_SCORE = 40


def search_posts(user_query: str, top_k: int = 5):
    collection = get_chroma_collection()

    print("🔎 Chroma indexed count:", collection.count())

    results = collection.query(
        query_texts=[user_query],
        n_results=5,
        include=["metadatas", "distances"]
    )

    ranked_results = []

    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    for metadata, distance in zip(metadatas, distances):
        verification_score = metadata.get("verification_score", 0)

        # 🔥 TEMPORARILY RELAX FILTER FOR DEMO
        # if verification_score < MIN_VERIFICATION_SCORE:
        #     continue

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

    ranked_results.sort(key=lambda x: x["final_score"], reverse=True)

    print("✅ Search returning", len(ranked_results), "results")

    return ranked_results[:top_k]
