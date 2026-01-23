from indexer import index_post
from chroma_client import get_chroma_collection

posts = [
    {
        "post_id": "p001",
        "practice_name": "Rooftop Rainwater Harvesting",
        "description": "Collecting rainwater from rooftops during monsoon",
        "region": "Karnataka",
        "principles": [
            "Gravity-based water collection",
            "First-flush diversion"
        ],
        "validation_score": 87
    },
    {
        "post_id": "p002",
        "practice_name": "Passive Cooling with Courtyards",
        "description": "Using airflow and shaded courtyards to cool homes",
        "region": "Rajasthan",
        "principles": [
            "Cross ventilation",
            "Thermal mass"
        ],
        "validation_score": 75
    }
]

for post in posts:
    index_post(post)

# 🔑 FORCE A READ
collection = get_chroma_collection()
print("Indexed count (same process):", collection.count())
