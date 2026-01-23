from search_engine.chroma_client import get_chroma_collection

collection = get_chroma_collection()

count = collection.count()
print("Number of indexed posts:", count)
