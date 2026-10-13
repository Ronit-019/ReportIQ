# ReportIQ

An end-to-end Retrieval-Augmented Generation (RAG) application for document intelligence, offline evaluation, and online observability.

ReportIQ lets users ask natural-language questions about indexed documents, inspect recorded evaluation results, and explore LangSmith traces through a unified Streamlit interface.

## Features

- **RAG Chat:** Ask questions about indexed documents and receive answers grounded in retrieved context.
- **Offline Evaluation Dashboard:** Review recorded evaluation metrics and baseline results.
- **Online Observability Dashboard:** Inspect LangSmith traces, request status, latency, and available request details.
- **Semantic Retrieval:** FAISS vector search with embeddings generated using `BAAI/bge-small-en-v1.5`.
- **LLM Generation:** Generate answers using the Groq API.
- **Document Processing:** Convert PDF documents to Markdown and prepare text chunks for retrieval.
- **Streamlit Interface:** Access the application's features from one Python-based web interface.

## Architecture

- **Interface:** Streamlit
- **RAG Framework:** LangChain
- **Embeddings:** Hugging Face Sentence Transformers
- **Vector Store:** FAISS
- **LLM Provider:** Groq API
- **Tracing and Observability:** LangSmith
- **Document Processing:** PyMuPDF and pymupdf4llm
- **Evaluation:** Recorded offline evaluation metrics and project evaluation scripts

## Project Structure

```text
ReportIQ/
├── app.py                              # Streamlit application
├── data/
│   ├── documents/                      # Source documents
│   └── processed/
│       ├── markdown/                   # Extracted Markdown documents
│       └── vectorstores/               # Local vector-store artifacts
├── evaluation/
│   └── results/                        # Recorded evaluation results
├── src/                                # Ingestion, chunking, retrieval and generation
├── tests/                              # Automated tests
├── requirements.txt                    # Python dependencies
└── README.md
```

Generated files and folders may be excluded from Git through `.gitignore`.

## Local Setup

### Prerequisites

- Python 3.13 or a compatible Python version
- Git
- A Groq API key
- A LangSmith API key for online observability

### 1. Clone the repository

```bash
git clone https://github.com/Ronit-019/ReportIQ.git
cd ReportIQ
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it in Git Bash on Windows:

```bash
source venv/Scripts/activate
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root for local development:

```dotenv
GROQ_API_KEY=your_groq_api_key
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=ReportIQ
```

Use your own credentials. Never commit `.env` or expose API keys in source control.

### 4. Prepare the vector store

The RAG pipeline may require pre-generated vector-store artifacts, including:

```text
data/processed/vectorstores/
├── v3_locked.faiss
└── v3_locked_chunks.pkl
```

These artifacts are excluded from Git. Ensure the matching files are available in the expected location, or regenerate them using the project's ingestion, chunking, embedding, and vector-store scripts.

The vector index and its corresponding chunks must be compatible with each other.

### 5. Run the Streamlit application

From the project root:

```bash
streamlit run app.py --server.fileWatcherType none
```

Streamlit will print a local URL, usually `http://localhost:8501`.

## Configuration

Configure these secrets in your local `.env` file or through the deployment platform's secrets settings:

| Variable | Purpose |
|---|---|
| `GROQ_API_KEY` | Access the Groq API for answer generation |
| `LANGSMITH_API_KEY` | Authenticate with LangSmith |
| `LANGSMITH_TRACING` | Enable LangSmith tracing |
| `LANGSMITH_PROJECT` | Specify the LangSmith project name |

The application should be tested without optional observability credentials if offline evaluation and chat are intended to work independently of LangSmith.

## Evaluation

ReportIQ includes recorded baseline evaluation results under `evaluation/results/`.

Evaluation results represent the experiments recorded in the repository. They should not be interpreted as guaranteed performance across all documents, questions, or datasets.

The golden evaluation dataset and its evaluation coverage may evolve as the project develops.

## Observability

The online observability dashboard uses LangSmith to retrieve available traces from the configured project.

The information displayed depends on the trace data recorded by the RAG pipeline and returned by LangSmith. Trace availability requires valid credentials, the correct project configuration, and tracing enabled for the relevant requests.

## Deployment

ReportIQ is designed to run as a Streamlit application. Streamlit Community Cloud can be used to host the interface and Python application.

Before deployment:

1. Push the required application code to GitHub.
2. Confirm that `requirements.txt` includes the application's dependencies.
3. Configure API keys through the deployment platform's secrets settings.
4. Ensure required vector-store artifacts and source data are available to the deployed application.
5. Test chat, evaluation metrics, and LangSmith observability after deployment.

Do not assume that files available only on a local computer will automatically be present in the hosted environment.

## Security Notes

- Never commit API keys, passwords, or `.env` files.
- Do not commit virtual environments, Python caches, or unnecessary generated artifacts.
- Protect private documents and any sensitive information included in prompts or traces.
- The source documents should only be distributed when you have permission to share them.

## License

No license has been specified. All rights reserved unless a license is added to this repository.