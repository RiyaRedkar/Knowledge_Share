from flask import Blueprint, render_template, request, redirect, url_for
import json, os, uuid
from datetime import datetime

post_bp = Blueprint("posts", __name__)

# --------------------
# INDEX (STEP 1)
# --------------------
@post_bp.route("/")
def index():
    return render_template("index.html")

# --------------------
# GENERATE (STEP 2)
# --------------------
@post_bp.route("/generate", methods=["POST"])
def generate_post():

    # Create draft
    draft = {
        "practice_name": request.form.get("practice_name", ""),
        "description": request.form.get("description", ""),
        "region": request.form.get("region", ""),
        "principles": [],
        "steps": [],
        "materials": [],
        "risks": [],
        "media": {
            "images": [],
            "videos": [],
            "documents": []
        }
    }

    # Assign post_id
    post_id = "p" + uuid.uuid4().hex[:6].upper()
    draft["post_id"] = post_id

    # Module 2 owns this
    draft["verification_score"] = 0

    # Save draft
    with open(f"uploads/posts/{post_id}_draft.json", "w") as f:
        json.dump(draft, f, indent=2)

    return render_template(
        "edit.html",
        post_id=post_id,
        draft_json=json.dumps(draft, indent=2)
    )

# --------------------
# SAVE (STEP 3)
# --------------------
@post_bp.route("/save/<post_id>", methods=["POST"])
def save_post(post_id):
    edited_json = request.form.get("edited_json")
    post = json.loads(edited_json)

    post["post_id"] = post_id
    post["verification_score"] = 0
    post["saved_at"] = datetime.utcnow().isoformat()

    with open(f"uploads/posts/{post_id}.json", "w") as f:
        json.dump(post, f, indent=2)

    return redirect(url_for("posts.demo"))

# --------------------
# DEMO (STEP 4)
# --------------------
@post_bp.route("/demo")
def demo():
    posts = []

    for file in os.listdir("uploads/posts"):
        if file.endswith(".json") and not file.endswith("_draft.json"):
            with open(os.path.join("uploads/posts", file)) as f:
                posts.append(json.load(f))

    return render_template("demo.html", posts=posts)
