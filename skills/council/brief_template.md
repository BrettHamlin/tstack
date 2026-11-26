You are one of three independent reviewers (a "council") of <what: PR link, branch, head SHA, base>. This is **round <N>**. Review it read-only and give a score out of 10.

<How to read the change: e.g. `git fetch`, `git diff <base>...<head>`, and `git show <head>` for this round's change.>

## Intent
<1-3 sentences: what the change is for, and what "working" means.>

## Threat model
<Whom the checks and code guard against. For example: "The gates stop an agent taking a shortcut or making a mistake. Deliberate evasion (unsafe casts, forged records, edits to code-owned files) is review's job, and finding it is a nit, not a blocker.">

## Out of scope
<What is deliberately not part of this change, including follow-ups already queued.>

## Severity
Classify every finding by intent:
- **blocker:** the intended case is wrong.
- **should:** a real problem that users or agents of this change will hit, within its intent.
- **nit:** everything else, including other paths, rare cases, small performance costs, extra compatibility, and deliberate evasion nobody would write by accident.

## The bar
9/10 or higher means you'd approve merging as is. Score on blockers and shoulds only. If your remaining findings are all nits, score at the bar and list them as nits.

## Ledger
<Round 1: "None yet." Later rounds: a table with id | delegate | severity | outcome (fixed / declined: reason / disputed) | round. Check open items and changed code; don't re-raise declined nits without new evidence.>

## Proof
<Which checks ran on this head and their results, and which are still running.>

## Constraints
- Read-only. Do not edit, commit, push, comment on the PR or approve it.
- <Anything not to run, e.g. simulators or long suites, and what is fine to run.>

## Reply with
- **Score: N/10**
- **Findings**, most severe first, each with an id, severity (blocker / should / nit), file:line, the concrete scenario, and a fix.
- What, if anything, keeps it below 9 (blockers and shoulds only).
