from flask import Blueprint, render_template, request, redirect, url_for
import os, json

from validation_module.utils import run_validation_for_post

# --------------------------------
# DEFINE BLUEPRINT FIRST (CRITICAL)
# --------------------------------
validation_bp = Blueprint("validation", __name__)

COMMENTS_DIR = "uploads/comments"

# --------------------------------
# RUN VALIDATION
# --------------------------------
@validation_bp.route("/validate/<post_id>", methods=["POST"])
def validate(post_id):
    run_validation_for_post(post_id)
    return redirect(url_for("posts.demo"))

# --------------------------------
# VIEW COMMENTS
# --------------------------------
@validation_bp.route("/comments/<post_id>")
def view_comments(post_id):
    comments_path = os.path.join(COMMENTS_DIR, f"{post_id}_comments.json")

    comments = []
    if os.path.exists(comments_path):
        with open(comments_path, "r", encoding="utf-8") as f:
            comments = json.load(f).get("comments", [])

    return render_template(
        "comments.html",
        post_id=post_id,
        comments=comments
    )

# --------------------------------
# ADD COMMENT
# --------------------------------
@validation_bp.route("/comments/<post_id>/add", methods=["POST"])
def add_comment(post_id):
    text = request.form.get("comment_text", "").strip()
    user_type = request.form.get("user_type", "opinion")

    if not text:
        return redirect(url_for("validation.view_comments", post_id=post_id))

    comments_path = os.path.join(COMMENTS_DIR, f"{post_id}_comments.json")

    data = {"comments": []}
    if os.path.exists(comments_path):
        with open(comments_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    data["comments"].append({
        "text": text,
        "user_type": user_type
    })

    with open(comments_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    return redirect(url_for("validation.view_comments", post_id=post_id))
