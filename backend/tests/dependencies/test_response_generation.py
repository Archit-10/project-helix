from app.dependencies.response_generation import (
    get_response_generation_service,
)
from app.services.response_generation import ResponseGenerationService


def test_get_response_generation_service():
    service = get_response_generation_service()

    assert isinstance(
        service,
        ResponseGenerationService,
    )
