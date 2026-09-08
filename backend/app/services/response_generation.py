from app.llm.base import LLM
from app.schemas.generation_response import GenerationResponse
from app.schemas.metadata_filter import MetadataFilter
from app.services.citation_generation import CitationGenerator
from app.services.prompt_builder import PromptBuilder
from app.services.retrieval import SemanticRetrievalService


class ResponseGenerationService:
    """Generates answers and citations using retrieved context and an LLM."""

    def __init__(
        self,
        retrieval_service: SemanticRetrievalService,
        prompt_builder: PromptBuilder,
        llm: LLM,
        citation_generator: CitationGenerator,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.prompt_builder = prompt_builder
        self.llm = llm
        self.citation_generator = citation_generator

    def generate(
        self,
        query: str,
        top_k: int,
        metadata_filter: MetadataFilter | None = None,
    ) -> GenerationResponse:
        results = self.retrieval_service.search(
            query=query,
            top_k=top_k,
            metadata_filter=metadata_filter,
        )

        prompt = self.prompt_builder.build(
            query=query,
            results=results,
        )

        answer = self.llm.generate(prompt)

        citations = self.citation_generator.generate(results)

        return GenerationResponse(
            answer=answer,
            citations=citations,
        )
