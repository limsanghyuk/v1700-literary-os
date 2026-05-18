from dataclasses import dataclass, field

@dataclass
class ProviderBoundary:
    default_provider_calls: int = 0
    allowed_adapters: list[str] = field(default_factory=list)

    def record_call(self, adapter: str) -> None:
        if adapter not in self.allowed_adapters:
            raise PermissionError(f"provider adapter not allowed: {adapter}")
        self.default_provider_calls += 1

    def assert_no_default_calls(self) -> None:
        if self.default_provider_calls != 0:
            raise AssertionError(f"provider default calls must be 0, got {self.default_provider_calls}")
