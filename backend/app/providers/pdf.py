from pathlib import Path

from pypdf import PdfReader

from app.providers.base import DocumentProvider


class PdfProvider(DocumentProvider):
    """Loads PDF documents."""

    SUPPORTED_EXTENSIONS = {".pdf"}

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    def extract_content(self, path: Path) -> str:
        reader = PdfReader(path)

        return "\n".join(page.extract_text() or "" for page in reader.pages)
