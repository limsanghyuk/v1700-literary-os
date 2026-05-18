import pytest

from v1700.provider_runtime.context import ProviderCallContext
from v1700.provider_runtime.release_policy import ReleaseProviderPolicy, ProviderReleasePolicyError


def test_release_policy_blocks_live_provider_and_raw_manuscript():
    policy = ReleaseProviderPolicy()
    with pytest.raises(ProviderReleasePolicyError):
        policy.validate_context(ProviderCallContext(release_mode=True, allow_live_provider_calls=True))
    with pytest.raises(ProviderReleasePolicyError):
        policy.validate_provider("claude", ProviderCallContext(release_mode=True))
