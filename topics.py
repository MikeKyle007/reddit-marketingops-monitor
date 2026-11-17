"""Rule-based topic detection for an approved, read-only Reddit monitoring bot.

A post can match multiple topics. Patterns are case-insensitive and only read
public text made available under the application's Reddit API authorization.
Adjust the patterns to suit your approved research scope.
"""
from __future__ import annotations

import re

# Platform plus technical-action patterns catch examples like "Marketo integration",
# "integrating HubSpot with Salesforce", and "Marketing Cloud Next setup"
# without tagging every generic Marketo mention as a platform integration.
_PLATFORM = r"(?:marketo|hubspot|marketing[\s-]+cloud[\s-]+next)"
_PLATFORM_ACTION = (
    r"(?:integrat\w*|implement\w*|configur\w*|set[\s-]?up|"
    r"deploy\w*|connect\w*|sync(?:hroniz\w*)?|migrat\w*)"
)

TOPIC_PATTERNS: dict[str, tuple[str, ...]] = {
    # Existing topics: preserved.
    "MOPs / Marketing Operations": (
        r"\bmops\b",
        r"\bmarketing[\s-]+operations\b",
        r"\bmarketing[\s-]+ops\b",
        r"\bmarketing[\s-]+operation\b",
        r"\bmarketingops\b",
    ),
    "Marketo": (
        r"\bmarketo\b",
        r"\badobe[\s-]+marketo[\s-]+engage\b",
    ),
    "Marketing Automation": (
        r"\bmarketing[\s-]+automation\b",
        r"\blead[\s-]+scoring\b",
        r"\blead[\s-]+nurturing\b",
        r"\bnurture[\s-]+campaign\b",
    ),
    "RevOps": (
        r"\brevops\b",
        r"\brevenue[\s-]+operations\b",
        r"\brevenue[\s-]+ops\b",
    ),
    "AI in Marketing": (
        r"\bai[\s-]+in[\s-]+marketing\b",
        r"\bai[\s-]+agents?\b",
        r"\bagentic[\s-]+ai\b",
        r"\bmarketing[\s-]+ai\b",
        r"\bllms?\b",
    ),

    # New areas requested for research.
    "Marketo Migration": (
        r"\bmarketo\b[\s\S]{0,100}\b(?:migrat\w*|replatform\w*|consolidat\w*|workspaces?[\s-]+merg\w*)\b",
        r"\b(?:migrat\w*|replatform\w*|consolidat\w*|workspaces?[\s-]+merg\w*)\b[\s\S]{0,100}\bmarketo\b",
    ),
    "Preference Center": (
        r"\bpreferences?[\s-]+cent(?:er|re)s?\b",
        r"\bsubscription[\s-]+(?:cent(?:er|re)|management|preferences?)\b",
        r"\b(?:email|communication)[\s-]+preferences?\b",
        r"\bopt[\s-]?in[\s-]+management\b",
    ),
    "GDPR Discussions": (
        r"\bgdpr\b",
        r"\bgeneral[\s-]+data[\s-]+protection[\s-]+regulation\b",
        r"\bdata[\s-]+subject[\s-]+access[\s-]+requests?\b",
        r"\bdsar\b",
        r"\bright[\s-]+to[\s-]+be[\s-]+forgotten\b",
        r"\blawful[\s-]+basis\b",
    ),
    "Marketing Strategy": (
        r"\bmarketing[\s-]+strateg(?:y|ies)\b",
        r"\bstrategic[\s-]+marketing\b",
        r"\b(?:go[\s-]+to[\s-]+market|gtm|demand[\s-]+gen(?:eration)?|campaign|content|abm|account[\s-]+based[\s-]+marketing)[\s-]+strateg(?:y|ies)\b",
        r"\bmarketing[\s-]+plan(?:ning)?\b",
    ),
    "AI Services": (
        r"\bai[\s-]+services?\b",
        r"\bai[\s-]+(?:consulting|consultancy|agenc(?:y|ies))\b",
        r"\b(?:generative[\s-]+ai|gen[\s-]*ai|llm)[\s-]+(?:consulting|services?)\b",
        r"\bai[\s-]+as[\s-]+a[\s-]+service\b",
        r"\bai[\s-]+implementation[\s-]+services?\b",
    ),
    "Martech Solutions": (
        r"\bmartech[\s-]+(?:solutions?|stacks?|platforms?|tools?|software)\b",
        r"\bmarketing[\s-]+technolog(?:y|ies)[\s-]+(?:solutions?|stacks?|platforms?|tools?)\b",
        r"\bmarketing[\s-]+tech[\s-]+solutions?\b",
        r"\bmartech[\s-]+(?:ecosystem|architecture)\b",
    ),
    "Inboxing": (
        r"\binboxing\b",
        r"\binbox[\s-]+placement\b",
        r"\bemail[\s-]+deliverability\b",
        r"\bsender[\s-]+reputation\b",
        r"\bspam[\s-]+(?:folder|filter(?:ing)?)\b",
        r"\b(?:ip|domain)[\s-]+warming\b",
        r"\b(?:spf|dkim|dmarc)\b",
        r"\bpostmaster[\s-]+tools?\b",
    ),
    "AI-Driven Automation & Personalization": (
        r"\b(?:ai|artificial[\s-]+intelligence|machine[\s-]+learning)[\s-]+(?:driven|powered|enabled|based|assisted)[\s-]+(?:marketing[\s-]+)?(?:automation|personali[sz]ation)\b",
        r"\bai[\s-]+(?:marketing[\s-]+)?(?:automation|personali[sz]ation)\b",
        r"\bpredictive[\s-]+personali[sz]ation\b",
        r"\bhyper[\s-]*personali[sz]ation\b",
        r"\bpersonali[sz]\w*[\s-]+(?:with|using)[\s-]+ai\b",
        r"\bautomated[\s-]+personali[sz]ation\b",
    ),
    "Platform Implementation & Integration": (
        r"\bplatform[\s-]+(?:implementation|integration|deployment|setup)\b",
        rf"\b{_PLATFORM}\b[\s\S]{{0,90}}\b{_PLATFORM_ACTION}\b",
        rf"\b{_PLATFORM_ACTION}\b[\s\S]{{0,90}}\b{_PLATFORM}\b",
        # The specific new Salesforce product is of interest even before an
        # implementation question is phrased explicitly.
        r"\bmarketing[\s-]+cloud[\s-]+next\b",
    ),
}

COMPILED_PATTERNS = {
    name: tuple(re.compile(pattern, re.IGNORECASE) for pattern in patterns)
    for name, patterns in TOPIC_PATTERNS.items()
}


def categorize(text: str) -> list[str]:
    """Return all matching topic labels; no API calls or saved user content."""
    return [
        category
        for category, patterns in COMPILED_PATTERNS.items()
        if any(pattern.search(text) for pattern in patterns)
    ]
