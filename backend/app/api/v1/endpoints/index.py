from pathlib import Path

from fastapi import APIRouter, Depends

from app.dependencies.indexing import get_indexing_service
from app.dependencies.ingestion import get_ingestion_service
from app.schemas.index_request import IndexRequest
from app.schemas.index_response import IndexResponse
from app.services.indexing import IndexingService
from app.services.ingestion import IngestionService

router = APIRouter()


@router.post(
    "/index",
    response_model=IndexResponse,
    summary="Index a document",
    description="Ingest and index a local document.",
)
async def index_document(
    request: IndexRequest,
    ingestion_service: IngestionService = Depends(
        get_ingestion_service,
    ),
    indexing_service: IndexingService = Depends(
        get_indexing_service,
    ),
) -> IndexResponse:
    document = ingestion_service.ingest(
        Path(request.path),
    )

    chunks, _ = indexing_service.index(document)

    return IndexResponse(
        document_id=document.metadata.content_hash,
        chunks_indexed=len(chunks),
    )
