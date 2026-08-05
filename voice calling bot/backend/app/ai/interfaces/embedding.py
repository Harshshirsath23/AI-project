from abc import ABC, abstractmethod
from typing import Optional

from app.ai.models.embedding import EmbeddingRequest, EmbeddingResponse


class EmbeddingProvider(ABC):
    """
    Abstract interface for Embedding providers.
    
    All embedding providers (Sentence Transformers, etc.) must implement this interface.
    This ensures provider-agnostic usage throughout the application.
    """

    @abstractmethod
    async def initialize(self, config: dict) -> None:
        """
        Initialize the embedding provider with configuration.
        
        Args:
            config: Provider-specific configuration dictionary
        """
        pass

    @abstractmethod
    async def generate_embedding(
        self,
        request: EmbeddingRequest,
    ) -> EmbeddingResponse:
        """
        Generate an embedding for a single text.
        
        Args:
            request: Embedding request with text and parameters
        
        Returns:
            EmbeddingResponse with embedding vector and metadata
        
        Raises:
            AIProviderError: If embedding generation fails
        """
        pass

    @abstractmethod
    async def generate_embeddings_batch(
        self,
        texts: list[str],
        model: Optional[str] = None,
    ) -> list[EmbeddingResponse]:
        """
        Generate embeddings for multiple texts in batch.
        
        This is more efficient than generating embeddings one at a time.
        
        Args:
            texts: List of texts to generate embeddings for
            model: Optional model name override
        
        Returns:
            List of EmbeddingResponse with embedding vectors
        
        Raises:
            AIProviderError: If batch embedding generation fails
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """
        Check if the provider is healthy and available.
        
        Returns:
            bool: True if provider is healthy, False otherwise
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """
        Cleanup resources used by the provider.
        """
        pass

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Get the name of the provider.
        
        Returns:
            str: Provider name (e.g., "sentence_transformers")
        """
        pass

    @property
    @abstractmethod
    def embedding_dimension(self) -> int:
        """
        Get the dimension of the embedding vectors.
        
        Returns:
            int: Embedding dimension (e.g., 768, 1536)
        """
        pass
