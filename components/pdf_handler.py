from typing import List
from PyPDF2 import PdfReader

def parse_page_numbers(page_input: str) -> List[int]:
    """
    Convert page range string like '1,3-5' to list of 0-indexed integers.
    Example: '1,3-4' → [0, 2, 3]
    """
    pages = set()
    if not page_input:
        return []

    ranges = page_input.split(",")
    for r in ranges:
        r = r.strip()
        if "-" in r:
            start, end = r.split("-")
            pages.update(range(int(start) - 1, int(end)))
        else:
            pages.add(int(r) - 1)
    return sorted(pages)


def extract_text_from_pdf(pdf_file, page_numbers: List[int] = None) -> str:
    """
    Extracts text from specified pages in a single PDF.
    If no page_numbers are given, extracts all pages.
    """
    full_text = ""
    reader = PdfReader(pdf_file)
    total_pages = len(reader.pages)

    selected_pages = page_numbers if page_numbers else range(total_pages)

    for i in selected_pages:
        if 0 <= i < total_pages:
            text = reader.pages[i].extract_text()
            if text:
                full_text += text + "\n"
    return full_text
