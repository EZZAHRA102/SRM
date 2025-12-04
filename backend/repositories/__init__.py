"""Repository layer for data access."""
from .base import BaseRepository
from .mock_repository import MockRepository

__all__ = ["BaseRepository", "MockRepository"]


