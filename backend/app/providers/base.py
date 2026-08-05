from abc import ABC, abstractmethod
from pathlib import Path

from app.schemas.normalized_document import NormalizedDocument
from app.utils.file_utils import build_document_metadata


class DocumentProvider(ABC):
    """Base class for document providers."""

    @abstractmethod
    def supports(self, path: Path) -> bool:
        """Return True if this provider supports the given file."""

    @abstractmethod
    def extract_content(self, path: Path) -> str:
        """Extract text content from the document."""

    def load(self, path: Path) -> NormalizedDocument:
        """Load a document and return its normalized representation."""

        content = self.extract_content(path)

        metadata = build_document_metadata(path, content)

        return NormalizedDocument(
            content=content,
            metadata=metadata,
        )
