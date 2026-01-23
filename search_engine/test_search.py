# test_search.py

from searcher import search_posts

query = "Managing kitchen waste at home"

results = search_posts(query)

for r in results:
    print(r)
