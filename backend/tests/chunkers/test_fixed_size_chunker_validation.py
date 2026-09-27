import pytest

from app.chunkers.fixed_size import FixedSizeChunker


def test_invalid_chunk_size():
    with pytest.raises(ValueError):
        FixedSizeChunker(chunk_size=0)


def test_negative_overlap():
    with pytest.raises(ValueError):
        FixedSizeChunker(
            chunk_size=100,
            chunk_overlap=-1,
        )


def test_overlap_greater_than_chunk_size():
    with pytest.raises(ValueError):
        FixedSizeChunker(
            chunk_size=100,
            chunk_overlap=100,
        )
