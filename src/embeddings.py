import json
import time
from pathlib import Path

from langchain_huggingface import HuggingFaceEmbeddings

MODEL = "BAAI/bge-small-en-v1.5"
CHUNKS_DIR = Path("data/processed/chunks")

start = time.time()

embeddings = HuggingFaceEmbeddings(
    model_name=MODEL
)

print(f"Model loaded in {time.time() - start:.1f}s")

for version in ["v1", "v3"]:
    chunks = json.loads(
        (CHUNKS_DIR / f"{version}.json").read_text(encoding="utf-8")
    )

    start = time.time()

    vectors = embeddings.embed_documents(
        [chunk["text"] for chunk in chunks]
    )

    print(
        f"{version}: "
        f"{len(chunks)} chunks, "
        f"{len(vectors[0])} dimensions, "
        f"{time.time() - start:.1f}s"
    )