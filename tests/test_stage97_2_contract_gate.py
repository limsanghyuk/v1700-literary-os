from v1700.provider_runtime import FixtureProvider, ProviderHealthMonitor, ProviderTaskRouter
from v1700.provider_runtime.contract_gate import ProviderAdapterContractGate


def test_provider_adapter_contract_gate_accepts_fixture_router():
    fixture = FixtureProvider()
    providers = {"fixture": fixture}
    router = ProviderTaskRouter(providers, ProviderHealthMonitor(providers, {"fixture": True}))
    result = ProviderAdapterContractGate().check([fixture], router)
    assert result["status"] == "pass"
    assert result["task_router_llm0_status"] == "pass"
