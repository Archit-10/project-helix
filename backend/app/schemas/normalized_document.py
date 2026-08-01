from pydantic import BaseModel

from app.schemas.document_metadata import DocumentMetadata


class NormalizedDocument(BaseModel):
    content: str
    metadata: DocumentMetadata
