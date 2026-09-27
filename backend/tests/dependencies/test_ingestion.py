from app.dependencies.ingestion import get_ingestion_service
from app.services.ingestion import IngestionService


def test_get_ingestion_service():
    get_ingestion_service.cache_clear()

    service = get_ingestion_service()

    assert isinstance(service, IngestionService)


def test_get_ingestion_service_is_cached():
    get_ingestion_service.cache_clear()

    first = get_ingestion_service()
    second = get_ingestion_service()

    assert first is second
