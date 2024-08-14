import re

from bs4 import BeautifulSoup

from .ruling_patterns import (
    after_review,
    court_acts,
    court_admin,
    granted_denied,
    hence_this,
    issue_errors,
    issue_resolution,
    main_issue,
    merit,
    resolve_issue,
    single_issue,
)


def ruling_cue(text: str) -> str | None:
    """Get first matching cue"""
    html = BeautifulSoup(text, "lxml")
    cues = iter(
        [
            after_review,
            court_acts,
            court_admin,
            granted_denied,
            hence_this,
            issue_errors,
            issue_resolution,
            main_issue,
            merit,
            resolve_issue,
            single_issue,
        ]
    )

    for cue in cues:
        pattern = re.compile(cue, re.X)
        if matches := html(string=pattern):
            initial = matches[0]
            return str(initial)

    return None
