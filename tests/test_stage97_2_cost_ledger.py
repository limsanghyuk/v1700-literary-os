from v1700.provider_runtime.cost_ledger import ProviderCostLedger
from v1700.provider_runtime.response import ProviderResponse


def test_provider_cost_ledger_records_unknown_cost_safely():
    ledger = ProviderCostLedger("S", 1)
    ledger.record_call(ProviderResponse(text="x", provider_id="claude", provider_kind="runtime", estimated_cost_usd=None))
    assert ledger.records["claude"].call_count == 1
    assert ledger.total_estimated_cost_usd is None
