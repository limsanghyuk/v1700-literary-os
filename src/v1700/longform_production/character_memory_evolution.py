from __future__ import annotations
from .contracts import CharacterMemoryPoint

def build_character_memory_evolution() -> dict:
    points = (
        CharacterMemoryPoint('protagonist','episode_01','guilt framed as forecasting error',0.10,'sibling_absence:unresolved','commit_guilt_seed'),
        CharacterMemoryPoint('protagonist','episode_08','admits active avoidance',0.22,'mother:truth_pressure','commit_avoidance_reversal'),
        CharacterMemoryPoint('protagonist','episode_16','chooses investigation over self-preservation',0.35,'institution:antagonistic','commit_agency_turn'),
        CharacterMemoryPoint('sibling_memory','episode_24','memory becomes contested evidence',0.18,'witness:emergent','commit_counter_memory'),
        CharacterMemoryPoint('protagonist','episode_32','integrates guilt with action plan',0.42,'community:restorative','commit_final_agency'),
    )
    return {'stage':'107.3','title':'Character Memory Evolution','status':'pass','memory_point_count':len(points),'agency_conservation_status':'pass','points':[p.to_dict() for p in points],'raw_manuscript_required':False,'provider_call_count':0}
