from collections.abc import Iterator

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.dependencies.response_generation import (
    get_response_generation_service,
)
from app.schemas.generation_response import GenerationResponse
from app.schemas.search_request import SearchRequest
from app.schemas.stream_event import StreamEvent
from app.services.response_generation import ResponseGenerationService

router = APIRouter()


def _stream_events(
    events: Iterator[StreamEvent],
) -> Iterator[str]:
    for event in events:
        yield f"data: {event.model_dump_json()}\n\n"


@router.post(
    "/generate",
    response_model=GenerationResponse,
    summary="Generate an answer",
    description="Generate an answer using retrieved context and the configured LLM.",
)
async def generate(
    request: SearchRequest,
    response_generation_service: ResponseGenerationService = Depends(
        get_response_generation_service,
    ),
) -> GenerationResponse:
    return response_generation_service.generate(
        query=request.query,
        top_k=request.top_k,
        metadata_filter=request.metadata_filter,
    )


@router.post(
    "/generate/stream",
    summary="Stream an answer",
    description="Stream an answer progressively using the configured LLM.",
)
async def generate_stream(
    request: SearchRequest,
    response_generation_service: ResponseGenerationService = Depends(
        get_response_generation_service,
    ),
) -> StreamingResponse:
    events = response_generation_service.generate_stream(
        query=request.query,
        top_k=request.top_k,
        metadata_filter=request.metadata_filter,
    )

    return StreamingResponse(
        _stream_events(events),
        media_type="text/event-stream",
    )
