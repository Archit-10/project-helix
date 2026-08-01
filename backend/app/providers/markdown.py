from pathlib import Path

from app.providers.base import DocumentProvider
from app.schemas.normalized_document import NormalizedDocument
from app.utils.file_utils import build_document_metadata


class MarkdownProvider(DocumentProvider):
    """Loads Markdown documents."""

    SUPPORTED_EXTENSIONS = {".md", ".markdown"}

    def supports(self, path: Path) -> bool:
        return path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    def load(self, path: Path) -> NormalizedDocument:
        content = path.read_text(encoding="utf-8")

        metadata = build_document_metadata(path, content)

        return NormalizedDocument(
            content=content,
            metadata=metadata,
        )
