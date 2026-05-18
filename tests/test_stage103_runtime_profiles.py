from v1700.stage103.runtime_profiles import build_runtime_profiles, validate_runtime_profiles


def test_stage103_runtime_profiles_are_separated_and_safe():
    profiles = {profile.profile_id: profile for profile in build_runtime_profiles()}
    assert set(profiles) == {"dev", "release", "sandbox"}
    assert profiles["release"].provider_mode == "fixture_or_mock_only"
    assert profiles["release"].allow_live_provider_calls is False
    assert profiles["sandbox"].credential_source == "explicit_env_only"


def test_stage103_runtime_profile_validation_passes():
    result = validate_runtime_profiles()
    assert result["status"] == "pass"
    assert result["release_profile_safe"] is True
    assert result["sandbox_opt_in_required"] is True
