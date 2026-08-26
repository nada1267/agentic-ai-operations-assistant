import os
import requests
import chromadb

from dotenv import load_dotenv


# ==========================================
# 1. Load environment variables
# ==========================================

load_dotenv()

JINA_API_KEY = os.getenv("JINA_API_KEY")

if not JINA_API_KEY:
    raise ValueError("JINA_API_KEY not found in .env")

print("JINA key loaded:", True)


# ==========================================
# 2. Connect to Chroma Server
# ==========================================

print("Connecting to Chroma Server...")

client = chromadb.HttpClient(
    host="127.0.0.1",
    port=8000
)

print("Connected to Chroma Server")


# ==========================================
# 3. Get collection
# ==========================================

collection = client.get_collection(
    name="company_policies",
    embedding_function=None
)

print("Collection found")


# ==========================================
# 4. Create Jina query embedding
# ==========================================

def get_query_embedding(query):

    response = requests.post(
        "https://api.jina.ai/v1/embeddings",

        headers={
            "Authorization": f"Bearer {JINA_API_KEY}",
            "Content-Type": "application/json"
        },

        json={
            "model": "jina-embeddings-v5-omni-small",
            "task": "retrieval.query",
            "input": [query]
        },

        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return data["data"][0]["embedding"]


# ==========================================
# 5. Retrieve relevant chunks
# ==========================================

def retrieve(query, top_k=3):

    print("\nQuery:")
    print(query)

    query_embedding = get_query_embedding(query)

    print("Query embedding created")
    print("Embedding size:", len(query_embedding))

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results


# ==========================================
# 6. Test Retriever
# ==========================================

if __name__ == "__main__":

    query = "What compensation is available for an order delayed 5 days?"

    results = retrieve(query, top_k=3)

    print("\n================================")
    print("Retrieved Results")
    print("================================")

    for i, document in enumerate(results["documents"][0]):

        print(f"\n--- Result {i + 1} ---")

        print(document)

        print("\nMetadata:")
        print(results["metadatas"][0][i])

        print("\nDistance:")
        print(results["distances"][0][i])