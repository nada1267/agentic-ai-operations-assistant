from pathlib import Path
import docx2txt

from langchain_core.documents import Document


KNOWLEDGE_DIR = Path("knowledge")


# Load TXT
txt_path = KNOWLEDGE_DIR / "company_policy.txt"

with open(txt_path, "r", encoding="utf-8") as file:
    txt_content = file.read()

txt_documents = [
    Document(
        page_content=txt_content,
        metadata={"source": str(txt_path)}
    )
]


# Load DOCX
docx_path = KNOWLEDGE_DIR / "Shipping_Policy.docx"

docx_content = docx2txt.process(str(docx_path))

docx_documents = [
    Document(
        page_content=docx_content,
        metadata={"source": str(docx_path)}
    )
]


# Combine documents
documents = txt_documents + docx_documents


# Chunking
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


for i, chunk in enumerate(chunks[:5]):

    print(f"\n--- Chunk {i + 1} ---")
    print(chunk.page_content)