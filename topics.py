"""Rule-based tagging of Marketing Operations conversations.

Edit TOPIC_PATTERNS to add more areas. Matching is case-insensitive.
"""
from __future__ import annotations

import re

TOPIC_PATTERNS: dict[str, tuple[str, ...]] = {
    "MOPs / Marketing Operations": (
        r"\bmops\b",                 # MOPs, mops, MOPS
        r"\bmarketing operations\b",
        r"\bmarketing ops\b",
        r"\bmarketing operation\b",
        r"\bmarketingops\b",
    ),
    "Marketo": (
        r"\bmarketo\b",
        r"\badobe marketo engage\b",
    ),
    "Marketing Automation": (
        r"\bmarketing automation\b",
        r"\blead scoring\b",
        r"\blead nurturing\b",
        r"\bnurture campaign\b",
    ),
    "RevOps": (
        r"\brevops\b",
        r"\brevenue operations\b",
        r"\brevenue ops\b",
    ),
    "AI in Marketing": (
        r"\bai in marketing\b",
        r"\bai agents?\b",
        r"\bagentic ai\b",
        r"\bmarketing ai\b",
        r"\bllms?\b",
    ),
}

COMPILED_PATTERNS = {
    name: tuple(re.compile(pattern, re.IGNORECASE) for pattern in patterns)
    for name, patterns in TOPIC_PATTERNS.items()
}


def categorize(text: str) -> list[str]:
    """Return all topic categories with matching keywords."""
    return [
        category
        for category, patterns in COMPILED_PATTERNS.items()
        if any(pattern.search(text) for pattern in patterns)
    ]
