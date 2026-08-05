from pathlib import Path

from app.providers.base import DocumentProvider


class TextProvider(DocumentProvider):
    """Loads plain text documents."""

    SUPPORTED_EXTENSIONS = {".txt"}

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    def extract_content(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")
