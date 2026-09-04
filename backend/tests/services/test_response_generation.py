from unittest.mock import Mock

from app.schemas.prompt import Prompt
from app.schemas.search_result import SearchResult
from app.services.response_generation import ResponseGenerationService


def create_search_result():
    return SearchResult(
        document_id="doc-1",
        chunk_id="chunk-1",
        score=0.95,
        content="Kafka uses SASL for authentication.",
    )


def test_generate():
    retrieval_service = Mock()
    prompt_builder = Mock()
    llm = Mock()

    results = [create_search_result()]

    prompt = Prompt(
        system_prompt="You are an engineering assistant.",
        user_prompt="How does Kafka authentication work?",
    )

    retrieval_service.search.return_value = results
    prompt_builder.build.return_value = prompt
    llm.generate.return_value = "Kafka uses SASL for authentication."

    service = ResponseGenerationService(
        retrieval_service=retrieval_service,
        prompt_builder=prompt_builder,
        llm=llm,
    )

    result = service.generate(
        query="How does Kafka authentication work?",
        top_k=5,
    )

    assert result == "Kafka uses SASL for authentication."

    retrieval_service.search.assert_called_once_with(
        query="How does Kafka authentication work?",
        top_k=5,
        metadata_filter=None,
    )

    prompt_builder.build.assert_called_once_with(
        query="How does Kafka authentication work?",
        results=results,
    )

    llm.generate.assert_called_once_with(prompt)
