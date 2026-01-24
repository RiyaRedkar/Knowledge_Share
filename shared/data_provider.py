# shared/data_provider.py

import json
from pathlib import Path
from typing import Dict, Iterator

# -----------------------------
# Paths (centralized here)
# -----------------------------

POSTS_DIR = Path("uploads/posts")
COMMENTS_DIR = Path("uploads/comments")


# -----------------------------
# Low-level loaders
# -----------------------------

def _load_json(path: Path) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_post(post_id: str) -> Dict:
    """
    Load a finalized post JSON by post_id.
    """
    path = POSTS_DIR / f"{post_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"Post not found: {path}")
    return _load_json(path)


def load_comments(post_id: str) -> Dict:
    """
    Load comments JSON for a post.
    Returns empty structure if not present.
    """
    path = COMMENTS_DIR / f"{post_id}_comments.json"
    if not path.exists():
        return {
            "post_id": post_id,
            "comments": [],
            "verification_score": 0
        }
    return _load_json(path)


# -----------------------------
# Normalization helpers
# -----------------------------

def normalize_for_search(post: Dict) -> Dict:
    """
    Normalize post fields so Search Engine
    always receives a consistent schema.
    """
    normalized = post.copy()

    # Search Engine expects 'validation_score'
    normalized["validation_score"] = post.get("verification_score", 0)

    return normalized


# -----------------------------
# Public providers
# -----------------------------

def iter_live_posts() -> Iterator[Dict]:
    """
    Iterate over all finalized posts
    ready for indexing/search.
    """
    if not POSTS_DIR.exists():
        return

    for path in POSTS_DIR.glob("*.json"):
        # Skip drafts explicitly
        if path.name.endswith("_draft.json"):
            continue

        post = _load_json(path)
        yield normalize_for_search(post)


def get_post_for_search(post_id: str) -> Dict:
    """
    Return post data needed for search indexing/ranking.
    """
    post = load_post(post_id)
    return normalize_for_search(post)


def get_post_for_adaptation(post_id: str) -> Dict:
    """
    Return full post content for Adaptation Engine.
    Adaptation does NOT need verification data.
    """
    return load_post(post_id)
