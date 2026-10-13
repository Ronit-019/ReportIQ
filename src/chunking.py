from pathlib import Path
import json
import re

from langchain_core.documents import Document
from langchain_text_splitters import (
    MarkdownHeaderTextSplitter,
    RecursiveCharacterTextSplitter,
)

MARKDOWN_DIR = Path("data/processed/markdown")
OUTPUT_DIR = Path("data/processed/chunks")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

PAGE_MARKER = re.compile(r"<!-- PDF_PAGE: (\d+) -->")


def load_documents():
    documents = []

    for file in MARKDOWN_DIR.glob("*.md"):
        content = file.read_text(encoding="utf-8")

        # Support the page-aware Markdown produced by ingestion.py.
        if PAGE_MARKER.search(content):
            parts = PAGE_MARKER.split(content)

            for index in range(1, len(parts), 2):
                page_number = int(parts[index])
                page_content = parts[index + 1].strip()

                if page_content:
                    documents.append(
                        Document(
                            page_content=page_content,
                            metadata={
                                "source": str(file),
                                "page": page_number,
                            },
                        )
                    )
        else:
            # Existing Markdown without page markers has unknown page numbers.
            documents.append(
                Document(
                    page_content=content,
                    metadata={"source": str(file)},
                )
            )

    return documents


def v3(documents):
    header_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3"),
        ],
        strip_headers=False,
    )

    sections = []

    for document in documents:
        parts = header_splitter.split_text(document.page_content)

        for part in parts:
            part.metadata.update(document.metadata)

        sections.extend(parts)

    # Merge short sections only when they belong to the same PDF page
    # and source document. This prevents chunks from losing page provenance.
    merged = []
    buffer = None

    for section in sections:
        if buffer is None:
            buffer = section
        elif (
            len(buffer.page_content) < 300
            and buffer.metadata.get("source") == section.metadata.get("source")
            and buffer.metadata.get("page") == section.metadata.get("page")
        ):
            buffer.page_content += "\n\n" + section.page_content

            for key in ("h1", "h2", "h3"):
                if section.metadata.get(key):
                    buffer.metadata[key] = section.metadata[key]
        else:
            merged.append(buffer)
            buffer = section

    if buffer:
        merged.append(buffer)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
    )

    return splitter.split_documents(merged)


documents = load_documents()
chunks = v3(documents)

output = OUTPUT_DIR / "v3_locked.json"

output.write_text(
    json.dumps(
        [
            {
                "text": chunk.page_content,
                "metadata": chunk.metadata,
            }
            for chunk in chunks
        ],
        indent=2,
        ensure_ascii=False,
    ),
    encoding="utf-8",
)

print(f"Documents/pages loaded: {len(documents)}")
print(f"Chunks created: {len(chunks)}")
print(f"Chunks with page metadata: {sum('page' in c.metadata for c in chunks)}")
print(f"Saved {len(chunks)} chunks -> {output}")
