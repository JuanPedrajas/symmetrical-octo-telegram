"""Gherkin parsing and compilation utilities.

parse_feature(text)   → structured dict  (serialise .feature → JSON)
compile_feature(data) → .feature string  (deserialise JSON → .feature)

Enforces Ebury tagging convention: every feature MUST carry
``@entry:<initiative>`` and ``@usecase:<slug>`` tags.
"""

from __future__ import annotations

from typing import Any

from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

Step = dict[str, str]  # {"keyword": "Given", "text": "..."}

Scenario = dict[str, Any]
# {
#   "name": str,
#   "tags": list[str],
#   "steps": list[Step],
# }

FeatureData = dict[str, Any]
# {
#   "feature": str,
#   "description": str,
#   "tags": list[str],
#   "background": list[Step],
#   "scenarios": list[Scenario],
# }


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _extract_tags(tag_nodes: list[dict]) -> list[str]:
    return [t["name"] for t in (tag_nodes or [])]


def _extract_steps(step_nodes: list[dict]) -> list[Step]:
    steps: list[Step] = []
    for s in step_nodes or []:
        keyword = s["keyword"].strip()
        steps.append({"keyword": keyword, "text": s["text"]})
    return steps


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def parse_feature(text: str) -> FeatureData:
    """Parse a ``.feature`` file text into a structured dict.

    Args:
        text: Full text content of a Gherkin ``.feature`` file.

    Returns:
        A dict with keys ``feature``, ``description``, ``tags``,
        ``background``, and ``scenarios``.

    Raises:
        gherkin.errors.ParserError: When the text is not valid Gherkin.
    """
    parser = Parser()
    gherkin_doc = parser.parse(TokenScanner(text))

    feature_node = gherkin_doc.get("feature", {})

    feature_name: str = feature_node.get("name", "")
    description: str = feature_node.get("description", "").strip()
    tags: list[str] = _extract_tags(feature_node.get("tags", []))

    background: list[Step] = []
    scenarios: list[Scenario] = []

    for child in feature_node.get("children", []):
        if "background" in child:
            bg = child["background"]
            background = _extract_steps(bg.get("steps", []))
        elif "scenario" in child:
            sc = child["scenario"]
            scenarios.append(
                {
                    "name": sc.get("name", ""),
                    "tags": _extract_tags(sc.get("tags", [])),
                    "steps": _extract_steps(sc.get("steps", [])),
                }
            )

    return {
        "feature": feature_name,
        "description": description,
        "tags": tags,
        "background": background,
        "scenarios": scenarios,
    }


def compile_feature(data: FeatureData) -> str:
    """Compile a structured dict back into a ``.feature`` file string.

    Enforces the Ebury tagging convention:
    - The ``tags`` list must contain at least one ``@entry:…`` tag.
    - The ``tags`` list must contain at least one ``@usecase:…`` tag.

    Args:
        data: A dict as returned by :func:`parse_feature`.

    Returns:
        A valid Gherkin ``.feature`` file string.

    Raises:
        ValueError: When required tags are missing.
    """
    tags: list[str] = data.get("tags", [])
    _validate_tags(tags)

    lines: list[str] = []

    # Feature-level tags on one line
    lines.append(" ".join(tags))

    # Feature header
    lines.append(f"Feature: {data['feature']}")

    # Description (indented)
    description = (data.get("description") or "").strip()
    if description:
        for desc_line in description.splitlines():
            lines.append(f"  {desc_line}" if desc_line.strip() else "")
        lines.append("")

    # Background
    background: list[Step] = data.get("background", [])
    if background:
        lines.append("  Background:")
        for step in background:
            lines.append(f"    {step['keyword']} {step['text']}")
        lines.append("")

    # Scenarios
    for scenario in data.get("scenarios", []):
        sc_tags: list[str] = scenario.get("tags", [])
        if sc_tags:
            lines.append(f"  {' '.join(sc_tags)}")
        lines.append(f"  Scenario: {scenario['name']}")
        for step in scenario.get("steps", []):
            lines.append(f"    {step['keyword']} {step['text']}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Internal validation
# ---------------------------------------------------------------------------

def _validate_tags(tags: list[str]) -> None:
    has_entry = any(t.startswith("@entry:") for t in tags)
    has_usecase = any(t.startswith("@usecase:") for t in tags)

    if not has_entry:
        raise ValueError(
            "Missing required @entry:<initiative> tag. "
            "Every feature must declare which initiative it belongs to."
        )
    if not has_usecase:
        raise ValueError(
            "Missing required @usecase:<slug> tag. "
            "Every feature must declare its use-case slug."
        )
