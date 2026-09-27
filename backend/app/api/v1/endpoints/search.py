from fastapi import APIRouter, Depends

from app.dependencies.retrieval import get_retrieval_service
from app.schemas.search_request import SearchRequest
from app.schemas.search_result import SearchResult
from app.services.hybrid_retrieval import HybridRetrievalService

router = APIRouter()


@router.post(
    "/search",
    response_model=list[SearchResult],
    summary="Search indexed documents",
    description="Search indexed documents using hybrid semantic and lexical retrieval.",
)
async def search(
    request: SearchRequest,
    retrieval_service: HybridRetrievalService = Depends(
        get_retrieval_service,
    ),
) -> list[SearchResult]:
    return retrieval_service.search(
        query=request.query,
        top_k=request.top_k,
        metadata_filter=request.metadata_filter,
    )
