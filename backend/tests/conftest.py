from datetime import UTC, datetime
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.schemas.document_metadata import DocumentMetadata


@pytest.fixture
def client():
    app = create_app()

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def metadata():
    return DocumentMetadata(
        file_name="test.txt",
        extension=".txt",
        path=Path("/tmp/test.txt"),
        size_bytes=100,
        last_modified=datetime.now(UTC),
        content_hash="test-hash",
    )
