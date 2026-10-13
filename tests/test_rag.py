import numpy as np
import pytest
from types import SimpleNamespace
from src import rag


def test_empty_question_is_rejected():
    with pytest.raises(ValueError, match="non-empty"):
        rag.ask("   ")


def test_pipeline_returns_expected_structure(monkeypatch):
    monkeypatch.setattr(
        rag,
        "embeddings",
        SimpleNamespace(
            embed_query=lambda question: [0.1, 0.2]
        ),
    )

    monkeypatch.setattr(
        rag.index,
        "search",
        lambda vector, k: (
            np.array([[0.2, 0.3, 0.4]], dtype="float32"),
            np.array([[0, 1, 2]], dtype="int64"),
        ),
    )

    monkeypatch.setattr(
        rag,
        "chunks",
        [
            {"text": "Context A", "metadata": {"source": "a.md"}},
            {"text": "Context B", "metadata": {"source": "b.md"}},
            {"text": "Context C", "metadata": {"source": "c.md"}},
        ],
    )

    monkeypatch.setattr(
        rag,
        "generate_answer",
        lambda question, contexts: "Test answer",
    )

    result = rag.ask("Test question")

    assert result["question"] == "Test question"
    assert result["answer"] == "Test answer"
    assert len(result["sources"]) == 3
    assert result["sources"][0]["rank"] == 1
    assert result["sources"][0]["metadata"]["source"] == "a.md"
    assert set(result["timings_ms"]) == {
        "embedding", "retrieval", "generation", "total"
    }


def test_empty_retrieval_skips_generation(monkeypatch):
    monkeypatch.setattr(
        rag,
        "embeddings",
        SimpleNamespace(
            embed_query=lambda question: [0.1, 0.2]
        ),
    )

    monkeypatch.setattr(
        rag.index,
        "search",
        lambda vector, k: (
            np.array([[float("inf")] * k], dtype="float32"),
            np.array([[-1] * k], dtype="int64"),
        ),
    )

    monkeypatch.setattr(rag, "chunks", [])

    def unexpected_generation(*args, **kwargs):
        pytest.fail("Generation should not run without retrieved chunks")

    monkeypatch.setattr(rag, "generate_answer", unexpected_generation)

    result = rag.ask("Unanswerable question")

    assert result["sources"] == []
    assert "not available" in result["answer"]
    assert result["timings_ms"]["generation"] == 0.0
