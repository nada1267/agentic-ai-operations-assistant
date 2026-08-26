import chromadb

client = chromadb.PersistentClient(
    path="rag/chroma_db"
)

collection = client.get_or_create_collection(
    name="company_policies"
)

print("ChromaDB is ready!")