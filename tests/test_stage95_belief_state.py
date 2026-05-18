from v1700.narrative_physics.belief_state import BeliefStateEngine


def test_stage95_belief_state_leakage_counter_is_explicit():
    engine = BeliefStateEngine()

    assert engine.leakage_count("safe surface") == 0
    assert engine.leakage_count("READER_ONLY: x RAW_REVEAL: y SECRET: z") == 3
