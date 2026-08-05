from pathlib import Path

from app.providers.base import DocumentProvider


class MarkdownProvider(DocumentProvider):
    """Loads Markdown documents."""

    SUPPORTED_EXTENSIONS = {".md", ".markdown"}

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    def extract_content(self, path: Path) -> str:
        return path.read_text(encoding="utf-8")
