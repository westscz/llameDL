from abc import ABC, abstractmethod
from functools import lru_cache


class BaseTagProvider(ABC):
    @lru_cache
    def get_tags_for(self, artist):
        """Return list of tags connected with delivered artist"""
        return self._get_tags_for(artist)

    @abstractmethod
    def _get_tags_for(self, artist):
        """Return list of tags connected with delivered artist"""
