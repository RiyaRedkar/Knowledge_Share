# adaptation_engine/adapter.py

import os
import json
from typing import Dict, Any

from dotenv import load_dotenv
from openai import OpenAI

from adaptation_engine.prompt import build_adaptation_prompt

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MAX_REFINEMENT_TURNS = 3


class AdaptationEngine:
    def __init__(self, post: Dict[str, Any]):
        self.post = post
        self.context_state = self._init_context_state()
        self.conversation_summary = ""
        self.refinement_turns = 0

    def _init_context_state(self) -> Dict[str, Any]:
        return {
            "location": "",
            "housing_type": "",
            "available_space": "",
            "budget_level": "",
            "constraints": [],
            "environmental_factors": {}
        }

    def update_context(self, updates: Dict[str, Any]):
        for key, value in updates.items():
            if "." in key:
                root, subkey = key.split(".", 1)
                self.context_state.setdefault(root, {})[subkey] = value
            else:
                self.context_state[key] = value

    def update_summary(self, summary: str):
        self.conversation_summary = summary.strip()

    def can_refine(self) -> bool:
        return self.refinement_turns < MAX_REFINEMENT_TURNS

    def adapt(self, user_feedback: str = "") -> Dict[str, Any]:
        if user_feedback and not self.can_refine():
            raise RuntimeError("Maximum refinement turns reached.")

        if user_feedback:
            self.refinement_turns += 1

        prompt = build_adaptation_prompt(
            post=self.post,
            context_state=self.context_state,
            conversation_summary=self.conversation_summary,
            user_feedback=user_feedback
        )

        response_text = self._call_openai(prompt)
        response = self._safe_json_parse(response_text)

        # Apply context updates
        if "context_updates" in response:
            self.update_context(response["context_updates"])

        # Update conversation summary
        if "conversation_summary" in response:
            self.update_summary(response["conversation_summary"])

        return response

    # -----------------------------
    # OpenAI integration
    # -----------------------------

    def _call_openai(self, prompt: str) -> str:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a structured reasoning engine."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )

        return completion.choices[0].message.content

    # -----------------------------
    # Safety
    # -----------------------------

    def _safe_json_parse(self, text: str) -> Dict[str, Any]:
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            raise ValueError(
                "Model response was not valid JSON. Response was:\n" + text
            )
