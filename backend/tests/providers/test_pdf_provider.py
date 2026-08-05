from pathlib import Path

from reportlab.pdfgen import canvas

from app.providers.pdf import PdfProvider


def create_sample_pdf(path: Path) -> None:
    pdf = canvas.Canvas(str(path))

    pdf.drawString(100, 750, "Project Helix")
    pdf.drawString(100, 730, "Enterprise Knowledge Platform")
    pdf.drawString(100, 710, "This PDF demonstrates document ingestion.")

    pdf.save()


def test_pdf_provider(tmp_path):
    pdf_path = tmp_path / "hello.pdf"

    create_sample_pdf(pdf_path)

    provider = PdfProvider()

    assert provider.supports(pdf_path)

    document = provider.load(pdf_path)

    assert document.metadata.file_name == "hello.pdf"
    assert document.metadata.extension == ".pdf"
    assert document.metadata.size_bytes > 0

    # SHA-256 hash
    assert len(document.metadata.content_hash) == 64

    # Extracted text
    assert "Project Helix" in document.content
    assert "Enterprise Knowledge Platform" in document.content
