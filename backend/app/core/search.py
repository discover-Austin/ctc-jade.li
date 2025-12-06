"""
Elasticsearch connection and management.
"""
from elasticsearch import AsyncElasticsearch
from typing import Optional
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)


class ElasticsearchClient:
    """Elasticsearch client wrapper."""

    def __init__(self):
        self.client: Optional[AsyncElasticsearch] = None

    async def connect(self) -> bool:
        """Initialize Elasticsearch connection."""
        try:
            self.client = AsyncElasticsearch(
                [settings.ELASTICSEARCH_URL],
                request_timeout=30,
                max_retries=3,
                retry_on_timeout=True
            )

            # Test connection
            await self.client.ping()
            logger.info("Elasticsearch connection established successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Elasticsearch: {e}")
            return False

    async def disconnect(self):
        """Close Elasticsearch connection."""
        if self.client:
            try:
                await self.client.close()
                logger.info("Elasticsearch connection closed successfully")
            except Exception as e:
                logger.error(f"Error closing Elasticsearch connection: {e}")

    async def check_connection(self) -> bool:
        """Check Elasticsearch connectivity."""
        if not self.client:
            return False

        try:
            return await self.client.ping()
        except Exception as e:
            logger.error(f"Elasticsearch connection check failed: {e}")
            return False

    async def create_index(self, index_name: str, body: dict) -> bool:
        """Create an index with mapping."""
        if not self.client:
            return False

        try:
            if not await self.client.indices.exists(index=index_name):
                await self.client.indices.create(index=index_name, body=body)
                logger.info(f"Created Elasticsearch index: {index_name}")
            return True
        except Exception as e:
            logger.error(f"Error creating Elasticsearch index: {e}")
            return False


# Global Elasticsearch client instance
es_client = ElasticsearchClient()


async def get_elasticsearch() -> Optional[AsyncElasticsearch]:
    """Dependency to get Elasticsearch client."""
    if es_client.client:
        return es_client.client
    return None
