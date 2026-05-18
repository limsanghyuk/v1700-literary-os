from v1700.longform_endurance.episode_planner import build_endurance_episode_plan
from v1700.longform_endurance.payoff_debt import build_payoff_debt_ledger


def test_stage97_payoff_debt_has_no_critical_default():
    report = build_payoff_debt_ledger(build_endurance_episode_plan(16))
    assert report["status"] == "pass"
    assert report["critical_debt_default_count"] == 0
    assert report["finale_unresolved_critical_debt"] == 0
