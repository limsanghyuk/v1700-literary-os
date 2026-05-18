from __future__ import annotations

from abc import ABC, abstractmethod

from .context import ProviderCallContext


class ProviderBridgeInterface(ABC):
    """All provider adapters must satisfy this exact Stage97.2 contract."""

    @abstractmethod
    def generate(self, prompt: str, context: ProviderCallContext) -> str:
        raise NotImplementedError

    @abstractmethod
    def is_available(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_provider_id(self) -> str:
        raise NotImplementedError
