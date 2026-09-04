from app.llm.base import LLM
from app.schemas.metadata_filter import MetadataFilter
from app.services.prompt_builder import PromptBuilder
from app.services.retrieval import SemanticRetrievalService


class ResponseGenerationService:
    """Generates answers using retrieved context and an LLM."""

    def __init__(
        self,
        retrieval_service: SemanticRetrievalService,
        prompt_builder: PromptBuilder,
        llm: LLM,
    ) -> None:
        self.retrieval_service = retrieval_service
        self.prompt_builder = prompt_builder
        self.llm = llm

    def generate(
        self,
        query: str,
        top_k: int,
        metadata_filter: MetadataFilter | None = None,
    ) -> str:
        results = self.retrieval_service.search(
            query=query,
            top_k=top_k,
            metadata_filter=metadata_filter,
        )

        prompt = self.prompt_builder.build(
            query=query,
            results=results,
        )

        return self.llm.generate(prompt)
