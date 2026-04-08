"""Tests for gherkin_parser.py — parse() and compile().

TDD Red → Green workflow:
  3.1 (Red)  — parser tests
  3.3 (Red)  — compiler tests
"""

import pytest

from app.utils.gherkin_parser import compile_feature, parse_feature

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

TEMPLATE_FEATURE = """\
@entry:npp @usecase:activate-account
Feature: Activate ASL account
  As a customer
  I want to activate my ASL account
  So that I can start using NPP payments

  Background:
    Given the NPP service is available
    And the customer has a valid BSB and account number

  @happy-path
  Scenario: Successfully activate an ASL account
    Given the customer is authenticated
    When the customer submits a valid activation request
    Then the ASL account is activated
    And the customer receives a confirmation

  @sad-path
  Scenario: Activation fails when service is unavailable
    Given the NPP service is unavailable
    When the customer submits an activation request
    Then the customer receives a service-unavailable error
"""

MINIMAL_FEATURE = """\
@entry:core @usecase:login
Feature: Login
  Background:
    Given the app is running

  Scenario: Happy path
    Given a valid user
    When the user logs in
    Then access is granted
"""


# ---------------------------------------------------------------------------
# parse_feature — structural tests
# ---------------------------------------------------------------------------


def test_parse_returns_top_level_keys():
    result = parse_feature(TEMPLATE_FEATURE)
    assert set(result.keys()) >= {"feature", "description", "tags", "background", "scenarios"}


def test_parse_feature_name():
    result = parse_feature(TEMPLATE_FEATURE)
    assert result["feature"] == "Activate ASL account"


def test_parse_feature_description():
    result = parse_feature(TEMPLATE_FEATURE)
    assert "customer" in result["description"]


def test_parse_feature_tags():
    result = parse_feature(TEMPLATE_FEATURE)
    assert "@entry:npp" in result["tags"]
    assert "@usecase:activate-account" in result["tags"]


def test_parse_background_steps():
    result = parse_feature(TEMPLATE_FEATURE)
    bg = result["background"]
    assert len(bg) == 2
    assert bg[0]["keyword"] in ("Given", "And", "But", "*")
    assert "NPP service is available" in bg[0]["text"]


def test_parse_scenarios_count():
    result = parse_feature(TEMPLATE_FEATURE)
    assert len(result["scenarios"]) == 2


def test_parse_scenario_name():
    result = parse_feature(TEMPLATE_FEATURE)
    assert result["scenarios"][0]["name"] == "Successfully activate an ASL account"


def test_parse_scenario_tags():
    result = parse_feature(TEMPLATE_FEATURE)
    assert "@happy-path" in result["scenarios"][0]["tags"]
    assert "@sad-path" in result["scenarios"][1]["tags"]


def test_parse_scenario_steps():
    result = parse_feature(TEMPLATE_FEATURE)
    steps = result["scenarios"][0]["steps"]
    keywords = [s["keyword"] for s in steps]
    assert "Given" in keywords
    assert "When" in keywords
    assert "Then" in keywords


def test_parse_minimal_feature():
    result = parse_feature(MINIMAL_FEATURE)
    assert result["feature"] == "Login"
    assert len(result["scenarios"]) == 1
    assert len(result["background"]) == 1


def test_parse_empty_background_when_absent():
    feature_no_bg = """\
@entry:x @usecase:y
Feature: No background

  Scenario: A scenario
    Given something
    Then it works
"""
    result = parse_feature(feature_no_bg)
    assert result["background"] == []


def test_parse_raises_on_invalid_gherkin():
    with pytest.raises(Exception):
        parse_feature("this is not valid gherkin !!!")


# ---------------------------------------------------------------------------
# compile_feature — output structure tests
# ---------------------------------------------------------------------------


def test_compile_returns_string():
    data = parse_feature(TEMPLATE_FEATURE)
    output = compile_feature(data)
    assert isinstance(output, str)


def test_compile_includes_feature_name():
    data = parse_feature(TEMPLATE_FEATURE)
    output = compile_feature(data)
    assert "Feature: Activate ASL account" in output


def test_compile_includes_entry_tag():
    data = parse_feature(TEMPLATE_FEATURE)
    output = compile_feature(data)
    assert "@entry:npp" in output


def test_compile_includes_usecase_tag():
    data = parse_feature(TEMPLATE_FEATURE)
    output = compile_feature(data)
    assert "@usecase:activate-account" in output


def test_compile_includes_background():
    data = parse_feature(TEMPLATE_FEATURE)
    output = compile_feature(data)
    assert "Background:" in output
    assert "NPP service is available" in output


def test_compile_includes_all_scenarios():
    data = parse_feature(TEMPLATE_FEATURE)
    output = compile_feature(data)
    assert "Successfully activate an ASL account" in output
    assert "Activation fails when service is unavailable" in output


def test_compile_includes_scenario_tags():
    data = parse_feature(TEMPLATE_FEATURE)
    output = compile_feature(data)
    assert "@happy-path" in output
    assert "@sad-path" in output


def test_compile_includes_steps():
    data = parse_feature(TEMPLATE_FEATURE)
    output = compile_feature(data)
    assert "Given the customer is authenticated" in output
    assert "When the customer submits a valid activation request" in output
    assert "Then the ASL account is activated" in output


def test_compile_raises_without_entry_tag():
    data = parse_feature(TEMPLATE_FEATURE)
    data["tags"] = ["@usecase:activate-account"]  # remove @entry
    with pytest.raises(ValueError, match="@entry"):
        compile_feature(data)


def test_compile_raises_without_usecase_tag():
    data = parse_feature(TEMPLATE_FEATURE)
    data["tags"] = ["@entry:npp"]  # remove @usecase
    with pytest.raises(ValueError, match="@usecase"):
        compile_feature(data)


def test_compile_roundtrip_preserves_data():
    """parse → compile → parse must yield equivalent data."""
    original = parse_feature(TEMPLATE_FEATURE)
    recompiled = compile_feature(original)
    roundtripped = parse_feature(recompiled)

    assert roundtripped["feature"] == original["feature"]
    assert set(roundtripped["tags"]) == set(original["tags"])
    assert len(roundtripped["background"]) == len(original["background"])
    assert len(roundtripped["scenarios"]) == len(original["scenarios"])


def test_compile_feature_description_preserved():
    data = parse_feature(TEMPLATE_FEATURE)
    output = compile_feature(data)
    assert "customer" in output


def test_compile_omits_background_section_when_empty():
    data = parse_feature(MINIMAL_FEATURE)
    data["background"] = []
    output = compile_feature(data)
    assert "Background:" not in output
