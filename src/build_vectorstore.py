import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings


CHUNKS_FILE = Path("data/processed/chunks/v3_locked.json")
VECTOR_DIR = Path("data/processed/vectorstores")

VECTOR_DIR.mkdir(parents=True, exist_ok=True)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)

chunks = json.loads(
    CHUNKS_FILE.read_text(encoding="utf-8")
)

vectors = np.array(
    embeddings.embed_documents(
        [chunk["text"] for chunk in chunks]
    ),
    dtype="float32",
)

index = faiss.IndexFlatL2(vectors.shape[1])
index.add(vectors)

faiss.write_index(
    index,
    str(VECTOR_DIR / "v3_locked.faiss"),
)

with open(VECTOR_DIR / "v3_locked_chunks.pkl", "wb") as f:
    pickle.dump(chunks, f)

print(f"Chunks: {len(chunks)}")
print(f"Dimensions: {vectors.shape[1]}")
print(f"Vectors in FAISS: {index.ntotal}")
print("Saved: v3_locked.faiss")
print("Saved: v3_locked_chunks.pkl")