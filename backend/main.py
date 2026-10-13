import json
from pathlib import Path
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from langsmith import Client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent.parent
EVALUATION_FILE = (
    ROOT / "evaluation" / "results" / "offline_evaluation_metrics.json"
)

app = FastAPI(title="ReportIQ API", version="1.0.0")

load_dotenv()

LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "ReportIQ")

class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


@app.get("/api/health")
def health():
    return {"status": "ok", "service": "ReportIQ API"}


@app.get("/api/evaluations")
def get_evaluations():
    if not EVALUATION_FILE.exists():
        raise HTTPException(
            status_code=404,
            detail="Offline evaluation metrics file was not found.",
        )

    try:
        return json.loads(EVALUATION_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as exc:
        raise HTTPException(
            status_code=500,
            detail="Could not read offline evaluation metrics.",
        ) from exc


@app.post("/api/chat")
def chat(request: ChatRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty.",
        )

    try:
        from src.rag import ask
        return ask(question)
    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail="RAG request failed. Check the backend terminal for details.",
        ) from exc

@app.get("/api/traces")
async def get_traces(limit: int = 50):
    limit = max(1, min(limit, 100))

    try:
        client = Client()

        projects = list(
            client.list_projects(name=LANGSMITH_PROJECT, limit=1)
        )

        if not projects:
            return {
                "project": LANGSMITH_PROJECT,
                "total": 0,
                "traces": [],
            }

        project_id = str(projects[0].id)

        fields = [
            "id",
            "name",
            "run_type",
            "status",
            "start_time",
            "end_time",
            "inputs",
            "outputs",
            "error",
        ]

        runs = [
            run
            async for run in client.runs.query(
                project_ids=[project_id],
                is_root=True,
                page_size=limit,
                selects=fields,
            )
        ]

        traces = []

        for run in runs:
            start = run.start_time
            end = run.end_time

            duration_ms = None
            if start and end:
                duration_ms = round(
                    (end - start).total_seconds() * 1000, 2
                )

            inputs = run.inputs or {}
            outputs = run.outputs or {}

            traces.append({
                "id": str(run.id),
                "name": run.name,
                "status": run.status,
                "start_time": start.isoformat() if start else None,
                "end_time": end.isoformat() if end else None,
                "duration_ms": duration_ms,
                "question": inputs.get("question"),
                "answer": outputs.get("answer"),
                "generation": outputs.get("generation", {}),
                "timings_ms": outputs.get("timings_ms", {}),
                "error": run.error,
            })

        traces.sort(
            key=lambda trace: trace["start_time"] or "",
            reverse=True,
        )

        return {
            "project": LANGSMITH_PROJECT,
            "total": len(traces),
            "traces": traces,
        }

    except Exception as exc:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=502,
            detail="Could not retrieve traces from LangSmith.",
        ) from exc