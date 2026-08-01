from abc import ABC, abstractmethod
from pathlib import Path

from app.schemas.normalized_document import NormalizedDocument


class DocumentProvider(ABC):
    """Base interface for all document providers."""

    @abstractmethod
    def supports(self, path: Path) -> bool:
        """
        Return True if this provider can process the given file.
        """
        raise NotImplementedError

    @abstractmethod
    def load(self, path: Path) -> NormalizedDocument:
        """
        Load a document and return a normalized representation.
        """
        raise NotImplementedError
