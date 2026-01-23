import os
import json

POSTS_DIR = "uploads/posts"
COMMENTS_DIR = "uploads/comments"

# -------------------------------
# SCORE FROM COMMENTS ONLY
# -------------------------------
def compute_validation_score(comments):
    if not comments:
        return 0

    total_weight = 0
    weighted_sum = 0

    for c in comments:
        text = c.get("text", "").strip()
        if not text:
            continue

        # very simple sentiment proxy (hackathon-safe)
        text_lower = text.lower()

        if any(word in text_lower for word in ["used", "experience", "years", "worked", "traditionally"]):
            sentiment = 1
            weight = 2   # experienced comment
        elif any(word in text_lower for word in ["good", "nice", "amazing", "useful"]):
            sentiment = 0.6
            weight = 1   # opinion comment
        else:
            sentiment = 0.3
            weight = 1

        weighted_sum += sentiment * weight
        total_weight += weight

    if total_weight == 0:
        return 0

    return round((weighted_sum / total_weight) * 100, 2)

# -------------------------------
# MAIN VALIDATION RUNNER
# -------------------------------
def run_validation_for_post(post_id):
    post_path = os.path.join(POSTS_DIR, f"{post_id}.json")
    comments_path = os.path.join(COMMENTS_DIR, f"{post_id}_comments.json")

    if not os.path.exists(comments_path):
        score = 0
    else:
        with open(comments_path, "r", encoding="utf-8") as f:
            comments = json.load(f).get("comments", [])

        score = compute_validation_score(comments)

    with open(post_path, "r", encoding="utf-8") as f:
        post = json.load(f)

    post["verification_score"] = score

    with open(post_path, "w", encoding="utf-8") as f:
        json.dump(post, f, indent=2)
