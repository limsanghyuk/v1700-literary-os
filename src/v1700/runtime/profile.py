from dataclasses import dataclass

@dataclass(frozen=True)
class RuntimeProfile:
    name: str = "local_first"
    external_provider_calls: int = 0
    provider_default_allowed: bool = False

    def assert_local_first(self) -> None:
        if self.name != "local_first":
            raise AssertionError(f"runtime profile must be local_first, got {self.name!r}")
        if self.external_provider_calls != 0:
            raise AssertionError("external provider calls must remain 0 by default")
        if self.provider_default_allowed:
            raise AssertionError("provider default routing must be disabled")
