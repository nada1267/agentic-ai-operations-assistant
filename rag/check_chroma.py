import chromadb

print("1 - Starting", flush=True)

client = chromadb.Client()

print("2 - Client created", flush=True)

collection = client.create_collection(
    name="test_collection"
)

print("3 - Collection created", flush=True)

collection.add(
    ids=["1"],
    documents=["This is a test document."]
)

print("4 - Document added", flush=True)

print("5 - Reading document...", flush=True)

result = collection.peek(limit=1)

print("6 - Read successful", flush=True)
print(result)