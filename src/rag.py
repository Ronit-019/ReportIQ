import json
import pickle
import time
from pathlib import Path
from langsmith import traceable
import faiss
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

from src.generator import generate_answer

ROOT = Path(__file__).resolve().parent.parent
VECTOR_DIR = ROOT / "data/processed/vectorstores"

MODEL = "BAAI/bge-small-en-v1.5"
TOP_K = 3

index = faiss.read_index(str(VECTOR_DIR / "v3_locked.faiss"))

with open(VECTOR_DIR / "v3_locked_chunks.pkl", "rb") as file:
    chunks = pickle.load(file)

_embeddings = None


def get_embeddings():
    global _embeddings

    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=MODEL)

    return _embeddings


@traceable(name="faiss_retrieval", run_type="retriever")
def retrieve_sources(query_vector):
    distances, indices = index.search(query_vector, TOP_K)

    return [
        {
            "text": chunks[i]["text"],
            "metadata": chunks[i]["metadata"],
            "distance": float(distance),
            "rank": rank,
        }
        for rank, (i, distance) in enumerate(
            zip(indices[0], distances[0]), start=1
        )
        if 0 <= i < len(chunks)
    ]


@traceable(name="reportiq_rag_request", run_type="chain")
def ask(question: str) -> dict:
    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question must be a non-empty string.")

    question = question.strip()
    total_start = time.perf_counter()

    start = time.perf_counter()
    query_vector = np.array(
        [get_embeddings().embed_query(question)],
        dtype="float32",
    )
    embedding_ms = (time.perf_counter() - start) * 1000

    start = time.perf_counter()
    sources = retrieve_sources(query_vector)
    retrieval_ms = (time.perf_counter() - start) * 1000
    
    generation_ms = 0.0
    generation_metadata = None

    if sources:
        generation_result = generate_answer(
            question,
            [source["text"] for source in sources],
        )

        answer = generation_result["answer"]
        generation_ms = generation_result["generation_ms"]

        generation_metadata = {
            "model": generation_result["model"],
            "tokens": generation_result["tokens"],
            "provider_request_id": generation_result["provider_request_id"],
        }
    else:
        answer = (
            "The information is not available in the provided context."
        )


    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "generation": generation_metadata,
        "timings_ms": {
            "embedding": round(embedding_ms, 2),
            "retrieval": round(retrieval_ms, 2),
            "generation": round(generation_ms, 2),
            "total": round(
                (time.perf_counter() - total_start) * 1000, 2
            ),
        },
    }


if __name__ == "__main__":
    result = ask("Where is Nexora Technologies headquartered?")
    print(json.dumps(result, indent=2, ensure_ascii=False))
