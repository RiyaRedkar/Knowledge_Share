import sys
from pathlib import Path

# Ensure project root is on PYTHONPATH
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from search_engine.indexer import index_post
from shared.data_provider import iter_live_posts


def main():
    count = 0

    for post in iter_live_posts():
        index_post(post)
        count += 1

    print(f"Indexed {count} live posts successfully.")


if __name__ == "__main__":
    main()

