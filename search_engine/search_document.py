# search_document.py

def build_search_document(post: dict) -> str:
    """
    Build the text that will be embedded for semantic search.
    """
    practice = post.get("practice_name", "")
    region = post.get("region", "")
    principles = ", ".join(post.get("principles", []))
    description = post.get("description", "")

    return (
        f"Practice: {practice}\n"
        f"Region: {region}\n"
        f"Core principles: {principles}\n"
        f"Use cases: {description}"
    )
