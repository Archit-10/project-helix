from app.schemas.search_result import SearchResult
from app.services.prompt_builder import PromptBuilder


def test_prompt_builder():
    results = [
        SearchResult(
            document_id="doc-1",
            chunk_id="chunk-1",
            score=0.95,
            content="Kafka uses SASL for client authentication.",
        ),
        SearchResult(
            document_id="doc-2",
            chunk_id="chunk-2",
            score=0.87,
            content="TLS can be used to encrypt Kafka connections.",
        ),
    ]

    builder = PromptBuilder()

    prompt = builder.build(
        query="How does Kafka authentication work?",
        results=results,
    )

    assert "Kafka uses SASL for client authentication." in prompt.user_prompt
    assert "TLS can be used to encrypt Kafka connections." in prompt.user_prompt
    assert "How does Kafka authentication work?" in prompt.user_prompt
    assert "engineering knowledge assistant" in prompt.system_prompt
