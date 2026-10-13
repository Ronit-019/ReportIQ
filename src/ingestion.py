from pathlib import Path

import pymupdf
import pymupdf4llm

PDF_DIR = Path("data/documents")
OUTPUT_DIR = Path("data/processed/markdown")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

for pdf in PDF_DIR.glob("*.pdf"):
    document = pymupdf.open(pdf)
    pages = []

    for page_number, page in enumerate(document, start=1):
        markdown = pymupdf4llm.to_markdown(
            document,
            pages=[page_number - 1],
        )

        pages.append(
            f"\n<!-- PDF_PAGE: {page_number} -->\n\n{markdown}"
        )

    output = OUTPUT_DIR / f"{pdf.stem}.md"
    output.write_text("\n".join(pages), encoding="utf-8")

    print(f"✓ {pdf.name} → {output.name} ({len(pages)} pages)")

    document.close()
