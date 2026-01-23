# test_search.py

from search_engine.searcher import search_posts

query = "Managing kitchen waste at home"

results = search_posts(query)

for r in results:
    print(r)
