from __future__ import annotations
from .contracts import PayoffCalendarItem

def build_payoff_calendar() -> dict:
    items = (
        PayoffCalendarItem('payoff_missing_sibling','episode_01','episode_16','DUE','WARN'),
        PayoffCalendarItem('payoff_false_forecast','episode_01','episode_08','PAID','INFO'),
        PayoffCalendarItem('payoff_institutional_cover','episode_12','episode_28','WATCH','WARN'),
        PayoffCalendarItem('payoff_childhood_witness','episode_06','episode_24','DUE','WARN'),
        PayoffCalendarItem('payoff_umbrella_object','episode_02','episode_31','WATCH','INFO'),
    )
    unresolved_blocks = [i.payoff_id for i in items if i.severity == 'BLOCK' and i.status != 'PAID']
    return {'stage':'107.4a','title':'Payoff Calendar','status':'pass' if not unresolved_blocks else 'blocked','unresolved_block_payoffs':unresolved_blocks,'payoff_count':len(items),'items':[i.to_dict() for i in items],'provider_call_count':0}
