from app.schemas.citation import Citation
from app.schemas.search_result import SearchResult


class CitationGenerator:
    """Generates citations from retrieved search results."""

    def generate(
        self,
        results: list[SearchResult],
    ) -> list[Citation]:
        return [
            Citation(
                document_id=result.document_id,
                chunk_id=result.chunk_id,
                file_name=result.metadata.file_name,
                path=result.metadata.path,
            )
            for result in results
        ]
