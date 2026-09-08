from unittest.mock import Mock

from app.schemas.citation import Citation
from app.schemas.prompt import Prompt
from app.schemas.search_result import SearchResult
from app.schemas.stream_event import StreamEvent
from app.services.response_generation import ResponseGenerationService


def create_search_result(metadata):
    return SearchResult(
        document_id="doc-1",
        chunk_id="chunk-1",
        score=0.95,
        content="Kafka uses SASL for authentication.",
        metadata=metadata,
    )


def test_generate(metadata):
    retrieval_service = Mock()
    prompt_builder = Mock()
    llm = Mock()
    citation_generator = Mock()

    results = [create_search_result(metadata)]

    prompt = Prompt(
        system_prompt="You are an engineering assistant.",
        user_prompt="How does Kafka authentication work?",
    )

    citations = [
        Citation(
            document_id="doc-1",
            chunk_id="chunk-1",
            file_name=metadata.file_name,
            path=metadata.path,
        )
    ]

    retrieval_service.search.return_value = results
    prompt_builder.build.return_value = prompt
    llm.generate.return_value = "Kafka uses SASL for authentication."
    citation_generator.generate.return_value = citations

    service = ResponseGenerationService(
        retrieval_service=retrieval_service,
        prompt_builder=prompt_builder,
        llm=llm,
        citation_generator=citation_generator,
    )

    result = service.generate(
        query="How does Kafka authentication work?",
        top_k=5,
    )

    assert result.answer == "Kafka uses SASL for authentication."
    assert result.citations == citations

    retrieval_service.search.assert_called_once_with(
        query="How does Kafka authentication work?",
        top_k=5,
        metadata_filter=None,
    )

    prompt_builder.build.assert_called_once_with(
        query="How does Kafka authentication work?",
        results=results,
    )

    citation_generator.generate.assert_called_once_with(results)

    llm.generate.assert_called_once_with(prompt)


def test_generate_stream(metadata):
    retrieval_service = Mock()
    prompt_builder = Mock()
    llm = Mock()
    citation_generator = Mock()

    results = [create_search_result(metadata)]

    prompt = Prompt(
        system_prompt="You are an engineering assistant.",
        user_prompt="How does Kafka authentication work?",
    )

    citations = [
        Citation(
            document_id="doc-1",
            chunk_id="chunk-1",
            file_name=metadata.file_name,
            path=metadata.path,
        )
    ]

    chunks = [
        "Kafka",
        " uses",
        " SASL",
        " for authentication.",
    ]

    retrieval_service.search.return_value = results
    prompt_builder.build.return_value = prompt
    llm.generate_stream.return_value = iter(chunks)
    citation_generator.generate.return_value = citations

    service = ResponseGenerationService(
        retrieval_service=retrieval_service,
        prompt_builder=prompt_builder,
        llm=llm,
        citation_generator=citation_generator,
    )

    result = list(
        service.generate_stream(
            query="How does Kafka authentication work?",
            top_k=5,
        )
    )

    assert result == [
        StreamEvent(type="token", content="Kafka"),
        StreamEvent(type="token", content=" uses"),
        StreamEvent(type="token", content=" SASL"),
        StreamEvent(
            type="token",
            content=" for authentication.",
        ),
        StreamEvent(
            type="citations",
            citations=citations,
        ),
        StreamEvent(type="done"),
    ]

    retrieval_service.search.assert_called_once_with(
        query="How does Kafka authentication work?",
        top_k=5,
        metadata_filter=None,
    )

    prompt_builder.build.assert_called_once_with(
        query="How does Kafka authentication work?",
        results=results,
    )

    llm.generate_stream.assert_called_once_with(prompt)

    citation_generator.generate.assert_called_once_with(results)
