import os

COUNTER_FILE = os.path.join("uploads", "posts", "counter.txt")

def get_next_post_id():
    # Ensure folder exists
    os.makedirs(os.path.dirname(COUNTER_FILE), exist_ok=True)

    # If counter file missing, create it
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("0")

    # Read current number
    with open(COUNTER_FILE, "r") as f:
        current = int(f.read().strip() or 0)

    # Increment
    next_num = current + 1

    # Save back
    with open(COUNTER_FILE, "w") as f:
        f.write(str(next_num))

    # Create serial post id
    return f"p{next_num:03d}"   # p001, p002, ...
