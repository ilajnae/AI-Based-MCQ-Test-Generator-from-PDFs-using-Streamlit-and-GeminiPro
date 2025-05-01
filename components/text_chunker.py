from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List

def split_text_into_chunks(text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
    """
    Splits long text into smaller overlapping chunks.
    
    Parameters:
        text (str): The full extracted text.
        chunk_size (int): Max size of each chunk.
        overlap (int): Overlap between consecutive chunks.

    Returns:
        List[str]: List of text chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " ", ""]
    )
    chunks = splitter.split_text(text)
    return chunks
