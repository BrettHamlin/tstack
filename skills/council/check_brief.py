#!/usr/bin/env python3
"""Check a council brief before it is sent.

Usage: python3 check_brief.py brief.md [--jev]

1. Structure (deterministic, blocking). The brief must have every section of brief_template.md, with no template
   placeholders left (`<...>`), and its severity section must define blocker, should and nit. Exit 1 if not.
2. Wording (Jev, advisory, with --jev). Typed true/false questions about the wording, asked of TypeSafe's Jev
   (POST https://api.typesafe.ai/v1/systemone, model pinned to jev-1.14.0). The key comes from $TYPESAFE_API_KEY or a
   file named by $TYPESAFE_API_KEY_FILE; it is never printed. Each question's probability is shown; >= 0.25 is flagged. On 11 test briefs (2026-11-17) a good template brief scored 0.04-0.07 on every question, and each planted bad sentence raised its question to 0.27-0.92; the cutoff was picked from that same data, so treat it as a starting point.
   Flags don't change the exit code: fix the brief, or note why a flag is a false alarm.
"""
import json
import os
import re
import sys
import urllib.request

FLAG_AT = 0.25
REQUIRED = ['## Intent', '## Threat model', '## Out of scope', '## Severity', '## The bar', '## Ledger', '## Proof',
            '## Constraints', '## Reply with']
SEVERITIES = ['**blocker:**', '**should:**', '**nit:**']

# Each question is answered true/false; True means the brief has the problem.
QUESTIONS = {
    'invites_adversarial_review': 'Does the brief ask reviewers to try hard to break, attack, defeat or find any possible '
                                  'bypass of the change, instead of judging it against its stated intent and threat model?',
    'claims_absolute_guarantees': 'Does the brief claim the change is airtight or works in any form or every possible '
                                  'case, rather than describing what is enforced and against whom?',
    'asks_beyond_scope': 'Does the brief ask reviewers to propose new features or review work outside the change it '
                         'describes?',
    'unclear_severity_use': 'Is it unclear from the brief that scores depend only on blockers and shoulds, and that '
                            'nits do not keep a score below the bar?',
}


def structure_problems(text: str) -> list[str]:
    problems = [f'missing section {s}' for s in REQUIRED if s not in text]
    problems += [f'severity section must define {s}' for s in SEVERITIES if s not in text]
    leftovers = re.findall(r'<[A-Za-z][^<>\n]*\s[^<>\n]*>', text)  # template placeholders contain a space; code like <module> doesn't
    problems += [f'template placeholder left: {p[:60]}' for p in leftovers]
    return problems


def jev_flags(text: str) -> dict[str, float]:
    key = os.environ.get('TYPESAFE_API_KEY')
    if not key and os.environ.get('TYPESAFE_API_KEY_FILE'):
        key = open(os.environ['TYPESAFE_API_KEY_FILE']).read().strip()
    if not key:
        raise SystemExit('--jev needs TYPESAFE_API_KEY or TYPESAFE_API_KEY_FILE')
    body = json.dumps({
        'model': 'jev-1.14.0',
        'state': {'review_brief': text},
        'questions': {name: {'type': 'noul', 'instructions': q} for name, q in QUESTIONS.items()},
    }).encode()
    request = urllib.request.Request('https://api.typesafe.ai/v1/systemone', data=body, method='POST', headers={
        'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=30) as response:
        answers = json.load(response).get('answers', {})
    return {name: float(answers[name]['noul']) for name in QUESTIONS}


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    text = open(sys.argv[1]).read()
    problems = structure_problems(text)
    for problem in problems:
        print(f'FAIL  {problem}')
    if not problems:
        print('PASS  structure: every required section present')
    if '--jev' in sys.argv[2:]:
        for name, probability in jev_flags(text).items():
            print(f'{"FLAG" if probability >= FLAG_AT else "ok  "}  {name}: {probability:.2f}')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
