from pathlib import Path
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

import app.main as main


def set_demo_directory(monkeypatch, tmp_path: Path) -> Path:
    monkeypatch.setattr(
        main,
        "__file__",
        str(tmp_path / "app" / "main.py"),
    )
    demo_dir = tmp_path / "demo-knowledge"
    demo_dir.mkdir(exist_ok=True)
    return demo_dir


def test_normal_startup_does_not_index_demo_documents(monkeypatch):
    monkeypatch.setattr(main.settings, "DEMO_MODE", False)
    monkeypatch.setattr(
        main,
        "get_ingestion_service",
        lambda: pytest.fail("Ingestion should not run in normal mode"),
    )
    monkeypatch.setattr(
        main,
        "get_indexing_service",
        lambda: pytest.fail("Indexing should not run in normal mode"),
    )

    with TestClient(main.create_app()):
        pass


def test_demo_startup_indexes_markdown_documents(monkeypatch, tmp_path):
    monkeypatch.setattr(main.settings, "DEMO_MODE", True)
    demo_dir = set_demo_directory(monkeypatch, tmp_path)

    (demo_dir / "b.md").write_text("# Document B", encoding="utf-8")
    (demo_dir / "a.md").write_text("# Document A", encoding="utf-8")

    ingestion_service = Mock()
    indexing_service = Mock()
    indexing_service.index.return_value = ([object()], [])

    monkeypatch.setattr(
        main,
        "get_ingestion_service",
        lambda: ingestion_service,
    )
    monkeypatch.setattr(
        main,
        "get_indexing_service",
        lambda: indexing_service,
    )

    with TestClient(main.create_app()):
        pass

    assert [call.args[0].name for call in ingestion_service.ingest.call_args_list] == [
        "a.md",
        "b.md",
    ]
    assert indexing_service.index.call_count == 2


def test_demo_startup_fails_if_directory_is_missing(monkeypatch, tmp_path):
    monkeypatch.setattr(main.settings, "DEMO_MODE", True)
    monkeypatch.setattr(
        main,
        "__file__",
        str(tmp_path / "app" / "main.py"),
    )

    with pytest.raises(RuntimeError, match="Demo knowledge directory not found"):
        with TestClient(main.create_app()):
            pass


def test_demo_startup_fails_if_directory_is_empty(monkeypatch, tmp_path):
    monkeypatch.setattr(main.settings, "DEMO_MODE", True)
    set_demo_directory(monkeypatch, tmp_path)

    with pytest.raises(RuntimeError, match="No Markdown documents found"):
        with TestClient(main.create_app()):
            pass
