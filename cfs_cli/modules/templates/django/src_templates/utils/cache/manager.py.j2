import logging
from threading import Lock
from typing import Set

from django.core.cache import cache

logger = logging.getLogger(__name__)


class CacheKeyManager:
    """Thread-safe cache key management with persistent registry"""

    _instance = None
    _lock = Lock()
    KEY_REGISTRY_PREFIX = 'cache_key_registry:'
    REGISTRY_TTL = 30 * 24 * 3600  # 30 days

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def register_key(self, key: str, category: str):
        """Register a cache key with thread-safe updates"""
        registry_key = f'{self.KEY_REGISTRY_PREFIX}{category}'
        try:
            with self._lock:
                keys = cache.get(registry_key, set())
                keys.add(key)
                cache.set(registry_key, keys, timeout=self.REGISTRY_TTL)
        except Exception as e:
            logger.error(f'Cache registration failed for {registry_key}: {e}', exc_info=True)

    def get_keys_by_category(self, category: str) -> Set[str]:
        """Get all keys for a category"""
        return cache.get(f'{self.KEY_REGISTRY_PREFIX}{category}', set())

    def invalidate_category(self, category: str):
        """Delete all cached keys in a category + clear registry"""
        registry_key = f'{self.KEY_REGISTRY_PREFIX}{category}'
        try:
            with self._lock:
                keys = cache.get(registry_key, set())
                for key in keys:
                    cache.delete(key)
                cache.delete(registry_key)
                logger.info(f"Invalidated {len(keys)} keys in category '{category}'")
        except Exception as e:
            logger.error(f'Failed to invalidate category {category}: {e}', exc_info=True)
