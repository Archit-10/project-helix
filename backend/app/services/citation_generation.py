from app.schemas.citation import Citation
from app.schemas.search_result import SearchResult


class CitationGenerator:
    """Generates unique document citations from retrieved search results."""

    def generate(
        self,
        results: list[SearchResult],
    ) -> list[Citation]:
        citations: list[Citation] = []
        seen_documents: set[str] = set()

        for result in results:
            if result.document_id in seen_documents:
                continue

            seen_documents.add(result.document_id)
            citations.append(
                Citation(
                    document_id=result.document_id,
                    chunk_id=result.chunk_id,
                    file_name=result.metadata.file_name,
                    path=result.metadata.path,
                )
            )

        return citations
