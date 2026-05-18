from __future__ import annotations
import hashlib, re
from .contracts import ProviderPromptPacket

SECRET_PATTERNS = [
    re.compile(r'sk-[A-Za-z0-9]{20,}'),
    re.compile(r'AKIA[0-9A-Z]{16}'),
    re.compile(r'AIza[0-9A-Za-z_-]{20,}'),
    re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
]
RAW_MARKERS = ('RAW_MANUSCRIPT', 'FULL_TEXT_MANUSCRIPT', '원고 전문', '<manuscript>')

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

def redact_prompt(text: str, max_chars: int = 6000) -> tuple[str, dict]:
    issues: list[str] = []
    redacted = text[:max_chars]
    for pattern in SECRET_PATTERNS:
        if pattern.search(redacted):
            issues.append('credential_pattern_detected')
            redacted = pattern.sub('[REDACTED_SECRET]', redacted)
    if any(marker.lower() in redacted.lower() for marker in RAW_MARKERS):
        issues.append('raw_manuscript_marker_detected')
    return redacted, {'status': 'pass' if not issues else 'blocked', 'issues': issues, 'prompt_sha256': sha256_text(text), 'redacted_chars': len(redacted)}

def make_prompt_packet(packet_id: str, provider_id: str, mode: str, prompt: str, max_output_tokens: int = 512) -> ProviderPromptPacket:
    _, info = redact_prompt(prompt)
    return ProviderPromptPacket(
        packet_id=packet_id,
        provider_id=provider_id,
        mode=mode,  # type: ignore[arg-type]
        payload_kind='FEATURE_ONLY',
        prompt_sha256=info['prompt_sha256'],
        raw_manuscript_included='raw_manuscript_marker_detected' in info['issues'],
        credential_included='credential_pattern_detected' in info['issues'],
        max_output_tokens=max_output_tokens,
    )
