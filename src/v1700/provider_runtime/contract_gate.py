from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Any

from .context import ProviderCallContext
from .interface import ProviderBridgeInterface
from .task_router import ProviderTaskRouter


@dataclass
class ContractViolation:
    adapter_class: str
    violation_type: str
    detail: str


class ProviderAdapterContractGate:
    """Stage97.2 contract gate for all provider adapters and routers."""

    def check(self, adapters: list[ProviderBridgeInterface], task_router: ProviderTaskRouter | None = None) -> dict[str, Any]:
        violations: list[ContractViolation] = []
        for adapter in adapters:
            violations.extend(self._check_signature(adapter))
            violations.extend(self._check_required_methods(adapter))
        if task_router is not None:
            violations.extend(self._check_router_llm0_compliance(task_router))
        return {
            "status": "pass" if not violations else "blocked",
            "adapters_checked": len(adapters),
            "violations": [v.__dict__ for v in violations],
            "task_router_llm0_status": "pass" if not [v for v in violations if v.violation_type == "llm0"] else "blocked",
        }

    def _check_signature(self, adapter: ProviderBridgeInterface) -> list[ContractViolation]:
        violations: list[ContractViolation] = []
        sig = inspect.signature(adapter.generate)
        params = list(sig.parameters.values())
        # Bound method signature should contain prompt, context.
        names = [p.name for p in params]
        if names[:2] != ["prompt", "context"]:
            violations.append(ContractViolation(adapter.__class__.__name__, "signature", f"generate parameters must be prompt, context; got {names}"))
        if any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params):
            violations.append(ContractViolation(adapter.__class__.__name__, "signature", "generate must not use **kwargs"))
        if "context" in sig.parameters:
            ann = sig.parameters["context"].annotation
            if ann not in {ProviderCallContext, "ProviderCallContext"}:
                violations.append(ContractViolation(adapter.__class__.__name__, "signature", f"context annotation must be ProviderCallContext; got {ann!r}"))
        return violations

    def _check_required_methods(self, adapter: ProviderBridgeInterface) -> list[ContractViolation]:
        violations: list[ContractViolation] = []
        for name in ("generate", "is_available", "get_provider_id"):
            if not callable(getattr(adapter, name, None)):
                violations.append(ContractViolation(adapter.__class__.__name__, "missing_method", name))
        try:
            provider_id = adapter.get_provider_id()
            if not isinstance(provider_id, str) or not provider_id:
                violations.append(ContractViolation(adapter.__class__.__name__, "provider_id", "provider id must be non-empty str"))
        except Exception as exc:
            violations.append(ContractViolation(adapter.__class__.__name__, "provider_id", str(exc)))
        return violations

    def _check_router_llm0_compliance(self, task_router: ProviderTaskRouter) -> list[ContractViolation]:
        before = {pid: getattr(provider, "generate_call_count", None) for pid, provider in task_router.providers.items()}
        try:
            task_router.route(ProviderCallContext(release_mode=True))
            task_router.route(ProviderCallContext(release_mode=False, narrative_fitness=0.88, provider_hint="quality"))
        except Exception as exc:
            return [ContractViolation(task_router.__class__.__name__, "llm0", f"route raised: {exc}")]
        after = {pid: getattr(provider, "generate_call_count", None) for pid, provider in task_router.providers.items()}
        if before != after:
            return [ContractViolation(task_router.__class__.__name__, "llm0", "route() invoked provider.generate()") ]
        return []
