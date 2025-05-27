import os
from pypdf import PdfReader
import nltk
import tiktoken

# Download tokenizer data
nltk.download("punkt")

class DocumentProcessor:
    def __init__(self, docs_path: str, chunk_size: int = 500, overlap: int = 100):
        self.docs_path = docs_path
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.tokenizer = tiktoken.get_encoding("cl100k_base")

    def _extract_text(self, path: str) -> str:
        reader = PdfReader(path)
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    def _tokenize(self, text: str) -> list[int]:
        return self.tokenizer.encode(text)

    def _decode(self, tokens: list[int]) -> str:
        return self.tokenizer.decode(tokens)

    def get_chunks(self) -> list[dict]:
        chunks = []
        for fname in sorted(os.listdir(self.docs_path)):
            if not fname.lower().endswith(".pdf"): continue
            full = os.path.join(self.docs_path, fname)
            text = self._extract_text(full)
            tokens = self._tokenize(text)
            i = 0
            cid = 0
            while i < len(tokens):
                window = tokens[i : i + self.chunk_size]
                chunks.append({
                    "id": f"{fname}_{cid}",
                    "doc_id": fname,
                    "chunk_id": cid,
                    "text": self._decode(window)
                })
                i += self.chunk_size - self.overlap
                cid += 1
        return chunks