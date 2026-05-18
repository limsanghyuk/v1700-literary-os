from v1700.provider_live_sandbox.payload_redactor import redact_prompt, make_prompt_packet

def test_payload_redactor_blocks_raw_and_secret():
    _, info = redact_prompt('RAW_MANUSCRIPT sk-abcdefghijklmnopqrstuvwxyz')
    assert info['status'] == 'blocked'
    packet = make_prompt_packet('p1','openai','PROSE','feature only premise')
    assert packet.raw_manuscript_included is False
    assert packet.credential_included is False
