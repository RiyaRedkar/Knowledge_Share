import json
from indexer import index_post

def normalize_score(score):
    # If score is between 0 and 1, convert to 1–100
    if score <= 1:
        return int(score * 100)
    return int(score)

with open("data/posts.json", "r") as f:
    posts = json.load(f)

for post in posts:
    post["validation_score"] = normalize_score(
        post["verification_score"]
    )
    index_post(post)

print(f"Indexed {len(posts)} posts successfully.")
