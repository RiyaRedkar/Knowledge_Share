from adapter import AdaptationEngine

sample_post = {
    "post_id": "p001",
    "practice_name": "Clay Pot Water Cooling",
    "description": "Traditional cooling using clay pots.",
    "principles": ["Evaporative cooling"],
    "risks": ["Requires airflow"]
}

engine = AdaptationEngine(sample_post)

print("=== Initial Adaptation ===")
response1 = engine.adapt()
print(response1)

print("\n=== Refinement ===")
response2 = engine.adapt(
    user_feedback="I live in a small apartment with an enclosed balcony and low airflow."
)
print(response2)
