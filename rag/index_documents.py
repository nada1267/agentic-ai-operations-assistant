from pathlib import Path
import os
import requests
import docx2txt
import chromadb

from dotenv import load_dotenv
from langchain_core.documents import Document


# ==========================================
# 1. Load environment variables
# ==========================================

load_dotenv()

JINA_API_KEY = os.getenv("JINA_API_KEY")

if not JINA_API_KEY:
    raise ValueError("JINA_API_KEY not found in .env")

print("JINA key loaded:", True)


# ==========================================
# 2. Load documents
# ==========================================

KNOWLEDGE_DIR = Path("knowledge")

documents = []


# TXT
txt_path = KNOWLEDGE_DIR / "company_policy.txt"

with open(txt_path, "r", encoding="utf-8") as file:
    txt_content = file.read()

documents.append(
    Document(
        page_content=txt_content,
        metadata={"source": str(txt_path)}
    )
)


# DOCX
docx_path = KNOWLEDGE_DIR / "Shipping_Policy.docx"

docx_content = docx2txt.process(str(docx_path))

documents.append(
    Document(
        page_content=docx_content,
        metadata={"source": str(docx_path)}
    )
)


# ==========================================
# 3. Chunking
# ==========================================

def split_text(text, chunk_size=500, chunk_overlap=50):

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - chunk_overlap

    return chunks


chunks = []

for document in documents:

    text_chunks = split_text(document.page_content)

    for chunk in text_chunks:

        chunks.append(
            Document(
                page_content=chunk,
                metadata=document.metadata
            )
        )


print(f"Loaded documents: {len(documents)}")
print(f"Created chunks: {len(chunks)}")


# ==========================================
# 4. Jina Embeddings
# ==========================================

def get_jina_embeddings(texts):

    response = requests.post(
        "https://api.jina.ai/v1/embeddings",

        headers={
            "Authorization": f"Bearer {JINA_API_KEY}",
            "Content-Type": "application/json"
        },

        json={
            "model": "jina-embeddings-v5-omni-small",
            "task": "retrieval.passage",
            "input": texts
        },

        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    return [
        item["embedding"]
        for item in data["data"]
    ]


texts = [
    chunk.page_content
    for chunk in chunks
]

print(f"Chunks to embed: {len(texts)}")


embeddings = get_jina_embeddings(texts)

print(f"Created embeddings: {len(embeddings)}")


# ==========================================
# 5. Connect to Chroma Server
# ==========================================

print("Connecting to Chroma Server...", flush=True)

client = chromadb.HttpClient(
    host="127.0.0.1",
    port=8000
)

print("Connected to Chroma Server!", flush=True)


# ==========================================
# 6. Get/Create Collection
# ==========================================

collection = client.get_or_create_collection(
    name="company_policies",
    embedding_function=None
)

print("Collection ready!", flush=True)


# ==========================================
# 7. Store embeddings in Chroma
# ==========================================

print("About to add embeddings to Chroma...", flush=True)

collection.add(
    ids=[
        f"chunk_{i}"
        for i in range(len(chunks))
    ],

    documents=texts,

    embeddings=embeddings,

    metadatas=[
        chunk.metadata
        for chunk in chunks
    ]
)

print("Embeddings added to Chroma!", flush=True)

print("Documents successfully indexed!", flush=True)


# ==========================================
# 8. Test Chroma
# ==========================================

print("Testing Chroma...", flush=True)

print("Collection count:", collection.count(), flush=True)

result = collection.peek(limit=2)

print("Chroma read successful!", flush=True)

print("IDs:")
print(result["ids"])

print("Documents:")
print(result["documents"])