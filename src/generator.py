from langsmith import traceable
import os
import time

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.environ["GROQ_API_KEY"])

MODEL = "openai/gpt-oss-120b"

@traceable(name="groq_generation", run_type="llm")
def generate_answer(question, contexts):
    context = "\n\n".join(
        f"[Context {i + 1}]\n{chunk}"
        for i, chunk in enumerate(contexts)
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a question-answering assistant for an internal "
                "company knowledge base. Answer the user's question using "
                "only the provided context. If the context does not contain "
                "the answer, say that the information is not available in "
                "the provided context. Do not use outside knowledge."
            ),
        },
        {
            "role": "user",
            "content": f"""Context:

{context}

Question:
{question}

Answer concisely using only the context above.""",
        },
    ]

    start = time.perf_counter()

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        reasoning_effort="low",
        temperature=0,
    )

    generation_ms = (time.perf_counter() - start) * 1000
    usage = response.usage

    return {
        "answer": response.choices[0].message.content or "",
        "model": response.model or MODEL,
        "generation_ms": round(generation_ms, 2),
        "tokens": {
            "input": usage.prompt_tokens if usage else None,
            "output": usage.completion_tokens if usage else None,
            "total": usage.total_tokens if usage else None,
        },
        "provider_request_id": getattr(response, "_request_id", None),
    }
