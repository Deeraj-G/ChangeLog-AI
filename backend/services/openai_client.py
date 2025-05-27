"""
OpenAI client management with singleton pattern and configuration.
"""

import os
from functools import lru_cache
from typing import Optional

from loguru import logger
from openai import OpenAI


class OpenAIClientManager:
    _instance: Optional[OpenAI] = None

    @classmethod
    @lru_cache(maxsize=1)
    def get_client(cls) -> OpenAI:
        """
        Get or create an OpenAI client instance using singleton pattern.
        Uses lru_cache to ensure we only create one instance per process.
        """
        if cls._instance is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OPENAI_API_KEY environment variable is not set")

            try:
                cls._instance = OpenAI(
                    api_key=api_key,
                    timeout=30.0,
                    max_retries=3,
                )
                logger.info("OpenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI client: {e}")
                raise

        return cls._instance

    @classmethod
    def reset_client(cls) -> None:
        """
        Reset the client instance. Useful for testing or when we need to
        reinitialize the client with new settings.
        """
        cls._instance = None
        cls.get_client.cache_clear()
