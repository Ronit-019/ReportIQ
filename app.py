import os
import time
from datetime import datetime, timezone
import json
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent
EVALUATION_FILE = (
    ROOT / "evaluation" / "results" / "offline_evaluation_metrics.json"
)


def run_rag_question(question: str) -> dict:
    """Call the existing RAG pipeline only when the user submits a question."""
    from src.rag import ask

    return ask(question)


def get_trace_client():
    """Create a LangSmith client when credentials are available."""
    from langsmith import Client

    api_key = os.getenv("LANGSMITH_API_KEY") or os.getenv("LANGCHAIN_API_KEY")
    if not api_key:
        raise ValueError(
            "LangSmith API key is missing. Configure LANGSMITH_API_KEY "
            "or LANGCHAIN_API_KEY in your local .env file."
        )

    return Client(api_key=api_key)


def get_trace_project() -> str:
    """Resolve the LangSmith project name."""
    return (
        os.getenv("LANGSMITH_PROJECT")
        or os.getenv("LANGCHAIN_PROJECT")
        or "default"
    )


def safe_text(value, fallback="Not available") -> str:
    """Convert trace fields into readable text."""
    if value is None:
        return fallback
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, default=str)


def extract_trace_field(data, *keys):
    """Find a useful field from common LangSmith input/output shapes."""
    if not isinstance(data, dict):
        return None

    for key in keys:
        if key in data and data[key] is not None:
            return data[key]

    return None


def trace_to_row(run) -> dict:
    """Normalize a LangSmith run for the dashboard table."""
    inputs = getattr(run, "inputs", None) or {}
    outputs = getattr(run, "outputs", None) or {}

    question = extract_trace_field(
        inputs, "question", "query", "input"
    )
    answer = extract_trace_field(
        outputs, "answer", "output", "response"
    )

    # Some LangChain traces store input/output under nested values.
    if question is None:
        question = extract_trace_field(inputs, "messages")
    if answer is None:
        answer = extract_trace_field(outputs, "messages")

    start_time = getattr(run, "start_time", None)
    end_time = getattr(run, "end_time", None)

    latency_seconds = None
    if start_time and end_time:
        latency_seconds = max(
            0.0, (end_time - start_time).total_seconds()
        )

    error = getattr(run, "error", None)

    return {
        "id": str(getattr(run, "id", "")),
        "name": getattr(run, "name", "Unnamed run"),
        "start_time": start_time,
        "status": "Error" if error else (
            "Completed" if end_time else "Running"
        ),
        "latency_seconds": latency_seconds,
        "question": safe_text(question),
        "answer": safe_text(answer),
        "error": safe_text(error, "") if error else "",
        "inputs": inputs,
        "outputs": outputs,
    }


def load_recent_traces(limit: int = 100) -> list[dict]:
    """Load recent root-level RAG requests from LangSmith."""
    client = get_trace_client()
    project_name = get_trace_project()

    runs = client.list_runs(
        project_name=project_name,
        is_root=True,
        limit=limit,
    )

    rows = [trace_to_row(run) for run in runs]

    # Newest requests first.
    rows.sort(
        key=lambda row: row["start_time"] or datetime.min.replace(
            tzinfo=timezone.utc
        ),
        reverse=True,
    )
    return rows


# --------------------------------------------------
# PAGE CONFIGURATION & STYLING
# --------------------------------------------------

st.set_page_config(
    page_title="ReportIQ | RAG Evaluation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    .reportiq-subtitle {
        color: #858b99;
        margin-top: -12px;
        margin-bottom: 25px;
    }

    .section-label {
        color: #858b99;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }

    .decision-card {
        border: 1px solid rgba(128, 128, 128, 0.25);
        border-radius: 12px;
        padding: 18px;
        margin: 8px 0 18px 0;
        line-height: 1.65;
    }

    .experiment-id {
        color: #858b99;
        font-size: 0.8rem;
        overflow-wrap: anywhere;
    }

    div[data-testid="stMetric"] {
        background: rgba(128, 128, 128, 0.07);
        border: 1px solid rgba(128, 128, 128, 0.16);
        padding: 15px;
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# LOAD EVALUATION DATA
# --------------------------------------------------

@st.cache_data
def load_evaluation_data(file_path: str, modified_time: float) -> dict:
    # modified_time is part of the cache key so edits to the JSON are detected.
    del modified_time

    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("The evaluation JSON root must be an object.")

    if not isinstance(data.get("experiments", []), list):
        raise ValueError("'experiments' must be a list.")

    return data


def humanize(value) -> str:
    return str(value).replace("_", " ").replace("-", " ").strip().title()


def format_metric_value(value, unit: str) -> str:
    if value is None:
        return "Not reported"

    if unit == "percent":
        return f"{value:g}%"

    if unit in ("ratio", "score") and isinstance(value, (int, float)):
        return f"{value:.3f}"

    if isinstance(value, float):
        return f"{value:g}"

    return str(value)


def outcome_badge(outcome: str) -> None:
    styles = {
        "selected": ("🟢", "Selected"),
        "retained": ("🟢", "Retained"),
        "passed": ("🟢", "Passed"),
        "baseline": ("🔵", "Baseline"),
        "rejected": ("🔴", "Rejected"),
        "pending": ("🟠", "Pending"),
        "inconclusive": ("🟡", "Inconclusive"),
    }

    emoji, label = styles.get(
        outcome.lower(),
        ("⚪", humanize(outcome)),
    )
    st.markdown(f"{emoji} **{label}**")


def get_experiment_metrics(record: dict) -> list[dict]:
    metrics = record.get("metrics", [])
    return metrics if isinstance(metrics, list) else []


# --------------------------------------------------
# NUMERIC METRIC CARDS
# --------------------------------------------------

def render_metric_cards(metrics: list[dict]) -> None:
    if not metrics:
        st.info("No numeric metrics have been recorded.")
        return

    variants = list(
        dict.fromkeys(
            str(metric.get("variant", "all"))
            for metric in metrics
        )
    )

    for variant in variants:
        variant_metrics = [
            metric
            for metric in metrics
            if str(metric.get("variant", "all")) == variant
        ]

        st.markdown(f"**Variant: {variant}**")

        numeric_metrics = [
            metric
            for metric in variant_metrics
            if isinstance(metric.get("value"), (int, float))
            and not isinstance(metric.get("value"), bool)
        ]

        if not numeric_metrics:
            st.caption("No numeric values reported for this variant.")
            continue

        for start in range(0, len(numeric_metrics), 4):
            group = numeric_metrics[start:start + 4]
            columns = st.columns(len(group))

            for column, metric in zip(columns, group):
                label = metric.get(
                    "label",
                    humanize(metric.get("name", "Metric")),
                )
                value = format_metric_value(
                    metric["value"],
                    metric.get("unit", ""),
                )

                with column:
                    st.metric(label=label, value=value)

        with st.expander(f"View {variant} metrics as a table"):
            rows = [
                {
                    "Metric": metric.get(
                        "label",
                        humanize(metric.get("name", "Metric")),
                    ),
                    "Value": metric.get("value"),
                    "Unit": metric.get("unit", "—"),
                    "Metric ID": metric.get("name", "—"),
                }
                for metric in variant_metrics
            ]

            st.dataframe(
                rows,
                width="stretch",
                hide_index=True,
            )


# --------------------------------------------------
# EXPERIMENT CARD
# --------------------------------------------------

def render_experiment(record: dict, index: int) -> None:
    experiment = record["experiment"]
    decision = record["decision"]
    metrics = get_experiment_metrics(record)

    name = experiment.get("name", f"Experiment {index}")
    experiment_id = experiment.get("id", "No ID")
    category = experiment.get("category", "uncategorized")
    status = experiment.get("status", "unknown")
    outcome = decision.get("outcome", "not_recorded")
    summary = decision.get(
        "summary",
        "No decision summary recorded.",
    )

    with st.container(border=True):
        # 1. EXPERIMENT
        title_col, status_col = st.columns([5, 1.5])

        with title_col:
            st.markdown(f"### {name}")
            st.markdown(
                f'<div class="experiment-id">{experiment_id}</div>',
                unsafe_allow_html=True,
            )

        with status_col:
            st.caption("Experiment status")
            st.write(humanize(status))
            st.caption("Decision outcome")
            outcome_badge(outcome)

        st.markdown("---")
        st.markdown(
            '<div class="section-label">1 · Experiment</div>',
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.caption("Category")
            st.write(humanize(category))

        with col2:
            st.caption("Status")
            st.write(humanize(status))

        with col3:
            st.caption("Numeric metrics")
            st.write(
                sum(
                    1
                    for metric in metrics
                    if isinstance(metric.get("value"), (int, float))
                    and not isinstance(metric.get("value"), bool)
                )
            )

        # 2. SUMMARY OF DECISION
        st.markdown("---")
        st.markdown(
            '<div class="section-label">2 · Summary of Decision</div>',
            unsafe_allow_html=True,
        )

        # Escape text before inserting it into HTML.
        import html

        st.markdown(
            f'<div class="decision-card">{html.escape(str(summary))}</div>',
            unsafe_allow_html=True,
        )

        # 3. NUMERIC METRICS
        st.markdown("---")
        st.markdown(
            '<div class="section-label">3 · Numeric Metrics</div>',
            unsafe_allow_html=True,
        )

        render_metric_cards(metrics)

        with st.expander("Technical details"):
            st.markdown("**Experiment record**")
            st.json(experiment)

            st.markdown("**Decision record**")
            st.json(decision)


# --------------------------------------------------
# HEADER AND NAVIGATION
# --------------------------------------------------

st.title("ReportIQ")
st.markdown(
    '<div class="reportiq-subtitle">'
    "RAG Evaluation & Observability Platform"
    "</div>",
    unsafe_allow_html=True,
)

offline_tab, chat_tab, observability_tab = st.tabs(
    [
        "📊 Offline Evaluation",
        "💬 RAG Chat",
        "🔎 Online Observability",
    ]
)


# --------------------------------------------------
# OFFLINE EVALUATION DASHBOARD
# --------------------------------------------------

with offline_tab:
    st.header("Offline Evaluation")
    st.caption(
        "Explore recorded experiments, understand decisions, "
        "and inspect measured retrieval and generation performance."
    )

    if not EVALUATION_FILE.exists():
        st.error(f"Evaluation file not found: {EVALUATION_FILE}")
    else:
        try:
            data = load_evaluation_data(
                str(EVALUATION_FILE),
                EVALUATION_FILE.stat().st_mtime,
            )

            raw_experiments = data.get("experiments", [])

            # Ignore malformed records, but preserve valid ones.
            records = [
                item
                for item in raw_experiments
                if isinstance(item, dict)
                and isinstance(item.get("experiment"), dict)
                and isinstance(item.get("decision"), dict)
            ]

            completed_count = sum(
                item["experiment"].get("status") == "completed"
                for item in records
            )

            rejected_count = sum(
                item["decision"].get("outcome") == "rejected"
                for item in records
            )

            selected_count = sum(
                item["decision"].get("outcome") == "selected"
                for item in records
            )

            # Overview — no pending-evaluation card.
            st.subheader("Evaluation Overview")

            overview = st.columns(3)
            overview[0].metric("Total Experiments", len(records))
            overview[1].metric("Completed", completed_count)
            overview[2].metric("Rejected Outcomes", rejected_count)

            st.caption(
                f"Project: {data.get('project', 'ReportIQ')} · "
                f"Schema version: {data.get('schema_version', 'N/A')} · "
                f"Selected outcomes: {selected_count}"
            )

            st.markdown("---")
            st.subheader("Explore Experiments")

            # Filters
            filter_col1, filter_col2, filter_col3 = st.columns(3)

            categories = sorted({
                item["experiment"].get("category", "uncategorized")
                for item in records
            })

            statuses = sorted({
                item["experiment"].get("status", "unknown")
                for item in records
            })

            outcomes = sorted({
                item["decision"].get("outcome", "not_recorded")
                for item in records
            })

            with filter_col1:
                selected_categories = st.multiselect(
                    "Category",
                    options=categories,
                    default=categories,
                    format_func=humanize,
                )

            with filter_col2:
                selected_statuses = st.multiselect(
                    "Experiment status",
                    options=statuses,
                    default=statuses,
                    format_func=humanize,
                )

            with filter_col3:
                selected_outcomes = st.multiselect(
                    "Decision outcome",
                    options=outcomes,
                    default=outcomes,
                    format_func=humanize,
                )

            search = st.text_input(
                "Search experiments",
                placeholder="Search experiment name, ID, or decision...",
            ).strip().lower()

            filtered_records = []

            for item in records:
                experiment = item["experiment"]
                decision = item["decision"]

                if experiment.get("category", "uncategorized") not in selected_categories:
                    continue

                if experiment.get("status", "unknown") not in selected_statuses:
                    continue

                if decision.get("outcome", "not_recorded") not in selected_outcomes:
                    continue

                searchable = " ".join([
                    str(experiment.get("name", "")),
                    str(experiment.get("id", "")),
                    str(decision.get("summary", "")),
                ]).lower()

                if search and search not in searchable:
                    continue

                filtered_records.append(item)

            st.caption(
                f"Showing {len(filtered_records)} of {len(records)} experiments."
            )

            if not filtered_records:
                st.info("No experiments match your selected filters.")
            else:
                for index, record in enumerate(filtered_records, start=1):
                    render_experiment(record, index)

            st.markdown("---")

            st.download_button(
                "Download Evaluation JSON",
                data=json.dumps(data, indent=2, ensure_ascii=False),
                file_name="offline_evaluation_metrics.json",
                mime="application/json",
            )

            with st.expander("About this evaluation record"):
                st.write(
                    "This dashboard displays the metrics and decisions "
                    "recorded in the JSON file; it does not recompute them. "
                    "Results from different benchmark configurations should "
                    "not be compared directly unless their evaluation setups "
                    "match."
                )

                # Keep other top-level metadata available, without a pending
                # evaluations section or a full JSON dump in the main view.
                metadata = {
                    key: value
                    for key, value in data.items()
                    if key not in ("experiments",)
                }
                st.json(metadata)

        except (OSError, json.JSONDecodeError, ValueError) as exc:
            st.error(f"Could not load evaluation data: {exc}")



# --------------------------------------------------
# RAG CHAT
# --------------------------------------------------

with chat_tab:
    st.header("RAG Chat")
    st.caption(
        "Ask questions about the indexed company documents. "
        "Answers are generated from retrieved context."
    )

    if "rag_messages" not in st.session_state:
        st.session_state.rag_messages = []

    if st.button("Clear conversation", key="clear_rag_chat"):
        st.session_state.rag_messages = []
        st.rerun()

    # Render conversation history.
    for message in st.session_state.rag_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if message["role"] == "assistant" and message.get("result"):
                result = message["result"]
                timings = result.get("timings_ms", {})

                with st.expander("Response metrics"):
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric(
                        "Embedding",
                        f'{timings.get("embedding", 0):,.0f} ms',
                    )
                    m2.metric(
                        "Retrieval",
                        f'{timings.get("retrieval", 0):,.0f} ms',
                    )
                    m3.metric(
                        "Generation",
                        f'{timings.get("generation", 0):,.0f} ms',
                    )
                    m4.metric(
                        "Total",
                        f'{timings.get("total", 0):,.0f} ms',
                    )

                    generation = result.get("generation") or {}
                    if generation:
                        st.caption(
                            f'Model: {generation.get("model", "Unknown")}'
                        )
                        tokens = generation.get("tokens") or {}
                        st.caption(
                            "Tokens — "
                            f'input: {tokens.get("input", "N/A")}, '
                            f'output: {tokens.get("output", "N/A")}, '
                            f'total: {tokens.get("total", "N/A")}'
                        )

                sources = result.get("sources") or []
                if sources:
                    with st.expander(
                        f"Retrieved sources ({len(sources)})"
                    ):
                        for source_index, source in enumerate(
                            sources, start=1
                        ):
                            metadata = source.get("metadata") or {}
                            st.markdown(
                                f"**Source {source_index} · "
                                f"Rank {source.get('rank', source_index)}**"
                            )
                            st.caption(
                                " · ".join(
                                    f"{key}: {value}"
                                    for key, value in metadata.items()
                                    if value is not None
                                ) or "No source metadata available"
                            )
                            st.write(source.get("text", ""))
                            st.divider()

    question = st.chat_input(
        "Ask a question about the company documents..."
    )

    if question and question.strip():
        question = question.strip()

        st.session_state.rag_messages.append(
            {"role": "user", "content": question}
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner(
                "Retrieving relevant documents and generating an answer..."
            ):
                try:
                    result = run_rag_question(question)
                    answer = result.get(
                        "answer",
                        "The RAG pipeline returned no answer.",
                    )

                    st.markdown(answer)

                    st.session_state.rag_messages.append(
                        {
                            "role": "assistant",
                            "content": answer,
                            "result": result,
                        }
                    )

                    timings = result.get("timings_ms", {})
                    m1, m2, m3, m4 = st.columns(4)
                    m1.metric(
                        "Embedding",
                        f'{timings.get("embedding", 0):,.0f} ms',
                    )
                    m2.metric(
                        "Retrieval",
                        f'{timings.get("retrieval", 0):,.0f} ms',
                    )
                    m3.metric(
                        "Generation",
                        f'{timings.get("generation", 0):,.0f} ms',
                    )
                    m4.metric(
                        "Total",
                        f'{timings.get("total", 0):,.0f} ms',
                    )

                    generation = result.get("generation") or {}
                    if generation:
                        st.caption(
                            f'Model: {generation.get("model", "Unknown")}'
                        )
                        tokens = generation.get("tokens") or {}
                        st.caption(
                            "Tokens — "
                            f'input: {tokens.get("input", "N/A")}, '
                            f'output: {tokens.get("output", "N/A")}, '
                            f'total: {tokens.get("total", "N/A")}'
                        )

                    sources = result.get("sources") or []
                    with st.expander(
                        f"Retrieved sources ({len(sources)})",
                        expanded=bool(sources),
                    ):
                        if not sources:
                            st.info("No sources were returned.")
                        for source_index, source in enumerate(
                            sources, start=1
                        ):
                            metadata = source.get("metadata") or {}
                            st.markdown(
                                f"**Source {source_index} · "
                                f"Rank {source.get('rank', source_index)}**"
                            )
                            st.caption(
                                " · ".join(
                                    f"{key}: {value}"
                                    for key, value in metadata.items()
                                    if value is not None
                                ) or "No source metadata available"
                            )
                            st.write(source.get("text", ""))
                            st.divider()

                except Exception as exc:
                    error_message = (
                        f"RAG request failed: {type(exc).__name__}: {exc}"
                    )
                    st.error(error_message)
                    st.caption(
                        "Check your .env credentials, vector-store files, "
                        "dependencies, and terminal logs."
                    )
                    st.session_state.rag_messages.append(
                        {
                            "role": "assistant",
                            "content": error_message,
                        }
                    )



# --------------------------------------------------
# ONLINE OBSERVABILITY
# --------------------------------------------------

with observability_tab:
    st.header("Online Observability")
    st.caption(
        "Inspect real RAG requests recorded in LangSmith, including "
        "request status, latency, errors, and input/output details."
    )

    top_left, top_right = st.columns([3, 1])

    with top_left:
        st.write(f"**LangSmith project:** `{get_trace_project()}`")

    with top_right:
        trace_limit = st.selectbox(
            "Requests to load",
            options=[25, 50, 100],
            index=2,
            key="trace_limit",
        )

    if st.button("Refresh traces", key="refresh_langsmith_traces"):
        st.session_state.pop("langsmith_trace_rows", None)

    if "langsmith_trace_rows" not in st.session_state:
        with st.spinner("Loading traces from LangSmith..."):
            try:
                st.session_state.langsmith_trace_rows = (
                    load_recent_traces(trace_limit)
                )
                st.session_state.langsmith_trace_error = None
            except Exception as exc:
                st.session_state.langsmith_trace_rows = None
                st.session_state.langsmith_trace_error = (
                    f"{type(exc).__name__}: {exc}"
                )

    # Reload if the user changes the requested trace limit.
    if st.session_state.get("loaded_trace_limit") != trace_limit:
        with st.spinner("Loading traces from LangSmith..."):
            try:
                st.session_state.langsmith_trace_rows = (
                    load_recent_traces(trace_limit)
                )
                st.session_state.langsmith_trace_error = None
            except Exception as exc:
                st.session_state.langsmith_trace_rows = None
                st.session_state.langsmith_trace_error = (
                    f"{type(exc).__name__}: {exc}"
                )
        st.session_state.loaded_trace_limit = trace_limit

    rows = st.session_state.get("langsmith_trace_rows")
    trace_error = st.session_state.get("langsmith_trace_error")

    if trace_error:
        st.error(f"Could not load LangSmith traces: {trace_error}")
        st.info(
            "Verify your LangSmith API key, project name, tracing settings, "
            "network connection, and that requests have been recorded."
        )

    elif not rows:
        st.info(
            "No root-level traces were found for this project yet. "
            "Submit a question in RAG Chat, ensure LangSmith tracing is "
            "enabled, then refresh this dashboard."
        )

    else:
        completed_rows = [
            row for row in rows if row["status"] == "Completed"
        ]
        error_rows = [row for row in rows if row["status"] == "Error"]
        latencies = [
            row["latency_seconds"]
            for row in rows
            if row["latency_seconds"] is not None
        ]

        avg_latency = (
            sum(latencies) / len(latencies) if latencies else None
        )

        st.markdown("---")
        st.subheader("Request Overview")

        metric_cols = st.columns(4)
        metric_cols[0].metric("Requests loaded", len(rows))
        metric_cols[1].metric("Completed", len(completed_rows))
        metric_cols[2].metric("Errors", len(error_rows))
        metric_cols[3].metric(
            "Average latency",
            f"{avg_latency:.2f} s" if avg_latency is not None else "N/A",
        )

        if latencies:
            st.caption(
                "Latency is calculated from each root trace's start and "
                "end timestamps. Only traces with both timestamps are used."
            )

        st.markdown("---")
        st.subheader("Recent Requests")

        status_filter = st.multiselect(
            "Filter by request status",
            options=["Completed", "Error", "Running"],
            default=["Completed", "Error", "Running"],
            key="trace_status_filter",
        )

        visible_rows = [
            row for row in rows if row["status"] in status_filter
        ]

        table_rows = [
            {
                "Started": (
                    row["start_time"].astimezone().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                    if row["start_time"] else "Unknown"
                ),
                "Request": row["name"],
                "Status": row["status"],
                "Latency (s)": (
                    round(row["latency_seconds"], 2)
                    if row["latency_seconds"] is not None else None
                ),
                "Question": row["question"][:180],
                "Trace ID": row["id"],
            }
            for row in visible_rows
        ]

        st.dataframe(
            table_rows,
            width="stretch",
            hide_index=True,
        )

        st.caption(
            f"Showing {len(visible_rows)} of {len(rows)} loaded requests."
        )

        st.markdown("---")
        st.subheader("Inspect a Trace")

        trace_options = {
            (
                f'{row["start_time"].strftime("%Y-%m-%d %H:%M:%S") if row["start_time"] else "Unknown time"}'
                f' · {row["name"]} · {row["id"][:8]}'
            ): row
            for row in rows
        }

        selected_trace_label = st.selectbox(
            "Select a request",
            options=list(trace_options.keys()),
            key="selected_trace_label",
        )

        if selected_trace_label:
            selected_trace = trace_options[selected_trace_label]

            detail_left, detail_right = st.columns(2)

            with detail_left:
                st.markdown("**Question / input**")
                st.write(selected_trace["question"])

            with detail_right:
                st.markdown("**Answer / output**")
                st.write(selected_trace["answer"])

            if selected_trace["error"]:
                st.error(selected_trace["error"])

            with st.expander("Full trace inputs and outputs"):
                st.markdown("**Inputs**")
                st.json(selected_trace["inputs"])

                st.markdown("**Outputs**")
                st.json(selected_trace["outputs"])

            with st.expander("Trace metadata"):
                st.json({
                    "trace_id": selected_trace["id"],
                    "run_name": selected_trace["name"],
                    "status": selected_trace["status"],
                    "start_time": safe_text(
                        selected_trace["start_time"]
                    ),
                    "latency_seconds": selected_trace["latency_seconds"],
                })

        st.download_button(
            "Download loaded trace summary",
            data=json.dumps(
                [
                    {
                        key: safe_text(value, "")
                        if isinstance(value, datetime) else value
                        for key, value in row.items()
                        if key not in ("inputs", "outputs")
                    }
                    for row in rows
                ],
                indent=2,
                ensure_ascii=False,
                default=str,
            ),
            file_name="reportiq_trace_summary.json",
            mime="application/json",
        )
