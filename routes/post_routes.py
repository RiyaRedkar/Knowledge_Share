import os
import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, send_from_directory

from services.id_service import get_next_post_id
from services.file_service import save_file
from services.stt_service import speech_to_text
from services.ai_draft_service import generate_ai_post_json

post_bp = Blueprint("post", __name__)

UPLOAD_FOLDER = "uploads"
POSTS_FOLDER = os.path.join(UPLOAD_FOLDER, "posts")
MEDIA_FOLDER = os.path.join(UPLOAD_FOLDER, "media")

os.makedirs(POSTS_FOLDER, exist_ok=True)
os.makedirs(MEDIA_FOLDER, exist_ok=True)


# ---------------------------
# ✅ Serve uploaded files (images/videos/docs)
# ---------------------------
@post_bp.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# ---------------------------
# ✅ HOME UI
# ---------------------------
@post_bp.route("/", methods=["GET"])
def home():
    return render_template("home.html")


# ---------------------------
# ✅ Create post form page
# ---------------------------
@post_bp.route("/create", methods=["GET"])
def create_post_page():
    return render_template("index.html")


# ---------------------------
# ✅ Generate Draft (AI)
# ---------------------------
@post_bp.route("/generate", methods=["POST"])
def generate():
    practice_name = request.form.get("practice_name", "").strip()
    region = request.form.get("region", "").strip()
    text_input = request.form.get("description", "").strip()

    audio_file = request.files.get("audio")
    image_file = request.files.get("image")
    video_file = request.files.get("video")
    doc_file = request.files.get("document")

    # ✅ Validation: either audio OR text must be present
    if (not text_input) and (not audio_file or audio_file.filename == ""):
        flash("Either Text Description OR Audio is required.")
        return redirect(url_for("post.create_post_page"))

    # Save media files
    media = {"images": [], "videos": [], "documents": []}

    image_path = save_file(image_file, MEDIA_FOLDER, "images")
    if image_path:
        media["images"].append(image_path)

    video_path = save_file(video_file, MEDIA_FOLDER, "videos")
    if video_path:
        media["videos"].append(video_path)

    doc_path = save_file(doc_file, MEDIA_FOLDER, "documents")
    if doc_path:
        media["documents"].append(doc_path)

    # Speech-to-text if audio present
    audio_text = ""
    if audio_file and audio_file.filename != "":
        audio_path = save_file(audio_file, MEDIA_FOLDER, "audio")
        audio_text = speech_to_text(audio_path)

    # ✅ Merge audio transcript + text
    if text_input and audio_text:
        combined_text = f"User Text:\n{text_input}\n\nElder Audio Transcript:\n{audio_text}"
    elif text_input:
        combined_text = text_input
    else:
        combined_text = audio_text

    # ✅ AI draft generated in AI service
    draft = generate_ai_post_json(
        practice_name=practice_name,
        region=region,
        combined_text=combined_text,
        media=media
    )

    # ✅ Assign serial post_id
    post_id = get_next_post_id()

    draft["post_id"] = post_id
    draft["practice_name"] = practice_name
    draft["region"] = region
    draft["media"] = media

    # ❌ Do NOT store draft json file
    return render_template(
    "edit.html",
    post_id=post_id,
    draft=draft
)


# ---------------------------
# ✅ Save Final Post JSON (ONLY ONE FILE)
# ---------------------------
@post_bp.route("/save/<post_id>", methods=["POST"])
def save(post_id):
    practice_name = request.form.get("practice_name", "").strip()
    region = request.form.get("region", "").strip()
    description = request.form.get("description", "").strip()

    # textarea list fields (one item per line)
    principles_text = request.form.get("principles", "").strip()
    steps_text = request.form.get("steps", "").strip()
    materials_text = request.form.get("materials", "").strip()
    risks_text = request.form.get("risks", "").strip()

    # convert line-separated text to lists
    principles = [x.strip() for x in principles_text.split("\n") if x.strip()]
    steps = [x.strip() for x in steps_text.split("\n") if x.strip()]
    materials = [x.strip() for x in materials_text.split("\n") if x.strip()]
    risks = [x.strip() for x in risks_text.split("\n") if x.strip()]

    # media comes hidden from edit.html
    media_json = request.form.get("media_json", "{}")
    try:
        media = json.loads(media_json)
    except:
        media = {"images": [], "videos": [], "documents": []}

    # verification score
    verification_score = request.form.get("verification_score", "0").strip()
    try:
        verification_score = int(float(verification_score))
    except:
        verification_score = 0

    # ✅ final JSON post
    final_post = {
        "post_id": post_id,
        "practice_name": practice_name,
        "description": description,
        "region": region,
        "principles": principles,
        "steps": steps,
        "materials": materials,
        "risks": risks,
        "media": media,
        "verification_score": verification_score,
        "saved_at": datetime.utcnow().isoformat() + "Z"
    }

    final_path = os.path.join(POSTS_FOLDER, f"{post_id}.json")
    with open(final_path, "w", encoding="utf-8") as f:
        json.dump(final_post, f, indent=2, ensure_ascii=False)

    flash(f"✅ Final Post Saved: {final_path}")
    return redirect(url_for("post.view_post", post_id=post_id))


# ---------------------------
# ✅ View All Posts (ONLY practice name)
# ---------------------------
@post_bp.route("/posts", methods=["GET"])
def list_posts():
    files = [
        f for f in os.listdir(POSTS_FOLDER)
        if f.endswith(".json") and not f.endswith("_draft.json")
    ]
    files.sort(reverse=True)

    posts_data = []
    for filename in files:
        post_id = filename.replace(".json", "")
        path = os.path.join(POSTS_FOLDER, filename)

        try:
            with open(path, "r", encoding="utf-8") as f:
                post_json = json.load(f)

            posts_data.append({
                "post_id": post_id,
                "practice_name": post_json.get("practice_name", post_id)
            })
        except Exception:
            posts_data.append({
                "post_id": post_id,
                "practice_name": post_id
            })

    return render_template("posts_list.html", posts=posts_data)


# ---------------------------
# ✅ View Single Post (Actual Post Preview)
# ---------------------------
@post_bp.route("/post/<post_id>", methods=["GET"])
def view_post(post_id):
    post_path = os.path.join(POSTS_FOLDER, f"{post_id}.json")

    if not os.path.exists(post_path):
        return "Post not found", 404

    with open(post_path, "r", encoding="utf-8") as f:
        post_data = json.load(f)

    return render_template("post_view.html", post=post_data)
