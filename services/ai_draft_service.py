import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_prompt(practice_name, region, combined_text, media):
    return f"""
You are an AI assistant generating a structured sustainability practice post.

Extract structured information and return JSON in this EXACT format:

{{
  "post_id": "pXXX",
  "practice_name": "{practice_name}",
  "description": "",
  "region": "{region}",
  "principles": [""],
  "steps": [""],
  "materials": [""],
  "risks": [""],
  "media": {{
    "images": [],
    "videos": [],
    "documents": []
  }},
  "verification_score": 0
}}

INPUT:
Combined Text:
{combined_text}

Media:
Images: {media.get("images", [])}
Videos: {media.get("videos", [])}
Documents: {media.get("documents", [])}

Rules:
- Make steps/materials/principles/risks meaningful.
- verification_score 0-100 based on completeness/clarity.
- media arrays must include given file paths if present.
Return ONLY VALID JSON.
"""

def generate_ai_post_json(practice_name, region, combined_text, media):
    """
    This function acts like an AI microservice.
    It can be reused later by other modules.
    """

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        # fallback draft if no key
        return {
            "post_id": "pXXX",
            "practice_name": practice_name,
            "description": combined_text[:500],
            "region": region,
            "principles": [""],
            "steps": [""],
            "materials": [""],
            "risks": [""],
            "media": media,
            "verification_score": 0
        }

    prompt = build_prompt(practice_name, region, combined_text, media)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Return only valid JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2
    )

    raw = response.choices[0].message.content.strip()

    try:
        return json.loads(raw)
    except:
        # If AI returns invalid JSON
        return {
            "post_id": "pXXX",
            "practice_name": practice_name,
            "description": combined_text[:500],
            "region": region,
            "principles": [""],
            "steps": [""],
            "materials": [""],
            "risks": [""],
            "media": media,
            "verification_score": 0
        }
