from flask import Blueprint, render_template, request, redirect, url_for
import json, os, uuid
from datetime import datetime

post_bp = Blueprint("posts", __name__)

# --------------------
# LANDING / NAV
# --------------------

@post_bp.route("/")
def landing():
    return render_template("landing.html")

@post_bp.route("/create")
def create_practice():
    return render_template("home.html")

# --------------------
# GENERATE (STEP 2)
# --------------------

@post_bp.route("/generate", methods=["POST"])
def generate_post():

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

    post_id = "p" + uuid.uuid4().hex[:6].upper()
    draft["post_id"] = post_id
    draft["verification_score"] = 0

    os.makedirs("uploads/posts", exist_ok=True)

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

    return redirect(url_for("posts.validate"))

# --------------------
# VALIDATE (STEP 4)
# --------------------

@post_bp.route("/validate")
@post_bp.route("/validate")
def validate():
    posts = []

    if os.path.exists("uploads/posts"):
        for file in os.listdir("uploads/posts"):
            if file.endswith(".json") and not file.endswith("_draft.json"):
                with open(os.path.join("uploads/posts", file)) as f:
                    posts.append(json.load(f))

    return render_template("demo.html", posts=posts)

# --------------------
# RUN VALIDATION (STEP 5)
# --------------------
@post_bp.route("/run_validation/<post_id>", methods=["POST"])
def run_validation(post_id):
    post_file = f"uploads/posts/{post_id}.json"
    comments_file = f"uploads/comments/{post_id}.json"

    if not os.path.exists(post_file):
        return "Post not found", 404

    with open(post_file) as f:
        post = json.load(f)

    # Load comments
    if os.path.exists(comments_file):
        with open(comments_file) as f:
            comments_data = json.load(f)
            comments = comments_data.get("comments", [])
    else:
        comments = []

    # Compute validation score
    score = compute_validation_score(comments)

    # Update post
    post["verification_score"] = score
    post["validated_at"] = datetime.utcnow().isoformat()

    with open(post_file, "w") as f:
        json.dump(post, f, indent=2)

    return redirect(url_for("posts.validate"))


# --------------------
# COMMENTS PAGE (STEP 6)
# --------------------

@post_bp.route("/comments/<post_id>", methods=["GET", "POST"])
def comments(post_id):
    comments_dir = "uploads/comments"
    os.makedirs(comments_dir, exist_ok=True)

    comments_file = os.path.join(comments_dir, f"{post_id}.json")

    # Load existing comments
    if os.path.exists(comments_file):
        with open(comments_file) as f:
            data = json.load(f)
    else:
        data = {
            "post_id": post_id,
            "comments": []
        }

    # Handle new comment submission
    if request.method == "POST":
        comment_text = request.form.get("comment")

        if comment_text:
            data["comments"].append({
                "text": comment_text,
                "created_at": datetime.utcnow().isoformat()
            })

            with open(comments_file, "w") as f:
                json.dump(data, f, indent=2)

        return redirect(url_for("posts.comments", post_id=post_id))

    return render_template(
        "comments.html",
        post_id=post_id,
        comments=data["comments"]
    )
def compute_validation_score(comments):
    """
    Simple heuristic-based validation score
    (can be replaced by NLP model later)
    """
    if not comments:
        return 0.0

    score = 0
    for c in comments:
        text = c["text"].lower()

        if any(x in text for x in ["used", "tried", "experience", "village", "years"]):
            score += 2        # experienced comment
        elif any(x in text for x in ["good", "useful", "effective"]):
            score += 1        # positive opinion
        elif any(x in text for x in ["bad", "useless", "outdated"]):
            score -= 1

    normalized = max(0, min(100, score * 10))
    return normalized

# --------------------
# ADAPTATION
# --------------------
@post_bp.route("/adapt/<post_id>", methods=["POST"])
def adapt(post_id):
    from adaptation_engine.adapter import AdaptationEngine
    from shared.data_provider import get_post_for_adaptation

    user_context = request.form.get("user_context", "").strip()

    # Load only the selected post
    post = get_post_for_adaptation(post_id)

    engine = AdaptationEngine(post)
    adapted_result = engine.adapt(user_context)

    return render_template(
        "demo.html",
        posts=[post],               # 🔥 ONLY THIS POST
        adapted_result=adapted_result,
        adapted_post_id=post_id,
        search_query=None
    )