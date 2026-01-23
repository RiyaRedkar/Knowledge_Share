# adaptation_engine/adapter.py

from typing import Dict, Any


MAX_REFINEMENT_TURNS = 3


class AdaptationEngine:
    """
    Post-anchored, context-aware adaptation engine.
    This engine adapts ONE traditional practice to a user's modern context.
    """

    def __init__(self, post: Dict[str, Any]):
        """
        Initialize the engine with a selected post.
        The post content NEVER changes.
        """
        self.post = post
        self.context_state = self._init_context_state()
        self.conversation_summary = ""
        self.refinement_turns = 0

    # -----------------------------
    # Context Management
    # -----------------------------

    def _init_context_state(self) -> Dict[str, Any]:
        """
        Initialize empty context state.
        """
        return {
            "location": "",
            "housing_type": "",
            "available_space": "",
            "budget_level": "",
            "constraints": [],
            "environmental_factors": {}
        }

    def update_context(self, updates: Dict[str, Any]):
        """
        Update context state using structured updates.
        Supports nested updates using dot-notation.
        """
        for key, value in updates.items():
            if "." in key:
                root, subkey = key.split(".", 1)
                if root not in self.context_state:
                    self.context_state[root] = {}
                self.context_state[root][subkey] = value
            else:
                self.context_state[key] = value

    def update_summary(self, summary: str):
        """
        Update conversation summary to avoid context drift.
        """
        self.conversation_summary = summary.strip()

    # -----------------------------
    # Safety & Control
    # -----------------------------

    def can_refine(self) -> bool:
        """
        Check whether more refinement turns are allowed.
        """
        return self.refinement_turns < MAX_REFINEMENT_TURNS

    # -----------------------------
    # Core Adaptation Interface
    # -----------------------------

    def adapt(self, user_feedback: str = "") -> Dict[str, Any]:
        """
        Perform one adaptation or refinement step.

        This function:
        - prepares input for the LLM
        - receives structured output
        - updates context
        - returns adapted solution

        NOTE:
        LLM call is NOT implemented yet.
        """
        if user_feedback and not self.can_refine():
            raise RuntimeError("Maximum refinement turns reached.")

        if user_feedback:
            self.refinement_turns += 1

        # Prepare payload for LLM (placeholder)
        payload = {
            "post": self.post,
            "context_state": self.context_state,
            "conversation_summary": self.conversation_summary,
            "user_feedback": user_feedback
        }

        # ---- PLACEHOLDER ----
        # This will be replaced with actual LLM call
        response = self._mock_llm_response(payload)

        # Update context if model suggests updates
        context_updates = response.get("context_updates", {})
        if context_updates:
            self.update_context(context_updates)

        # Update conversation summary if provided
        if "conversation_summary" in response:
            self.update_summary(response["conversation_summary"])

        return response

    # -----------------------------
    # Mock / Placeholder Logic
    # -----------------------------

    def _mock_llm_response(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Temporary mock response for testing the engine logic.
        This WILL be replaced by an LLM-backed implementation.
        """
        return {
            "adapted_solution": (
                f"Adaptation for '{self.post.get('practice_name')}' "
                f"based on current user context."
            ),
            "how_to_apply": [
                "Analyze available space",
                "Apply the practice at a reduced scale"
            ],
            "modern_modifications": [
                "Use compact materials suitable for apartments"
            ],
            "materials_needed": [
                "Locally available alternatives"
            ],
            "estimated_cost": "Low to Medium",
            "warnings": [
                "May not work effectively if airflow is limited"
            ],
            "context_updates": {},
            "conversation_summary": (
                "User is exploring how this traditional practice can "
                "fit their modern living constraints."
            )
        }
