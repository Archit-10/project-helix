from fastapi import APIRouter, Depends

from app.dependencies.response_generation import (
    get_response_generation_service,
)
from app.schemas.generation_response import GenerationResponse
from app.schemas.search_request import SearchRequest
from app.services.response_generation import ResponseGenerationService

router = APIRouter()


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
    answer = response_generation_service.generate(
        query=request.query,
        top_k=request.top_k,
        metadata_filter=request.metadata_filter,
    )

    return GenerationResponse(answer=answer)
