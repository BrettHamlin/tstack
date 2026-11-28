---
name: full-send
description: Trigger this if the user says 'full send'.
---

# Full Send

If the user triggered this, it's because they are not watching this thread, and
they want you to complete the work end-to-end autonomously. Your updates and
your final message go unread until long after you stop. You own the work from
its current state to a merged PR.

If the user did not explicitly request "full send" in some clear way, do not
assume full autonomy. If they did, everything below applies.

The user grants you permission to:

- Merge the PR once the merge gate passes.
- Force-push the PR's own branch with `--force-with-lease` after a rebase.
- Use the test methods that Proof needs, without asking first.
- Open, but not merge, the PRs that `correction-loop` makes in step 8: a rule
  PR in b-stack, and a follow-up PR in this repo.

## Testing permission

A "full send" request is the permission. If a project file or other
instruction says to ask before a test method, or to leave testing to the
user, this request replaces that rule for this task.

That includes ask-first rules for computer use, browser automation,
simulators and devices, running the app or a dev server, screenshots, and
visual checks. Use the method that gives direct proof. List it in the
report.

Rules about how to test still apply. Follow rules that name the correct
command, fixture, or check. This permission only removes the ask-first or
leave-it-to-the-user step. If a preferred method cannot prove the change,
use a gated method under this permission.

It covers only the tests needed for this task. It does not add permission
for the steps under "Asking the user", such as production changes or data
deletion. It also does not bypass a harness or system approval prompt if
one appears.

## Steps

1. **Finish the change.** Complete the goal from the user's request with the
   smallest real fix: one that fixes the cause, not one that only makes a
   check pass. Hardcoded or copied outputs, special cases for a test's input,
   stubs, skipped tests, and swallowed errors are not fixes. Fix the case that
   happened, not every case that could. Then search for the same mistake
   elsewhere: fix it if it is inside the goal, otherwise list each place in the
   report. If you are on the default branch, create a branch first.
   If the work is a new app and the `new-project` skill is installed, build
   it with that skill, so the repo starts from a b-stack starter.
2. **Prove it.** Get proof for every change you made. See "Proof".
3. **Check the tests did not get weaker.** Use the `test-integrity` skill on
   the change: its scan, then a judge from another model family. Apply every
   REPLACE and REVERT before review.
4. **Get feedback.** Use the `sol-loop` skill to verify changes. Put the
   `test-integrity` rulings in its brief's Checks line, so Sol doesn't ask to
   remove a test the judge required. After `sol-loop`, run the `test-integrity`
   scan again and judge any new flags.
5. **File the PR** with the `file-pr` skill. Load it with your harness's skill
   tool and follow it as written: its layout, diagrams, and evidence rules.
   Never write the title or description from memory. If a PR already exists
   for the branch, use `file-pr` to rewrite its title and description. Rebase
   onto the latest default branch first. Put how you proved the change in the
   description's Validation section.
6. **Babysit the PR** with the `babysit-pr` skill. Fix real findings and CI
   failures. Get proof for each fix before you push it. When a push changes
   the behavior, the review guide, or the proof, run `file-pr` again to update
   the description. After every fix, run the `test-integrity` scan again and
   judge any new flags before you push.
7. **Merge** when the merge gate passes.
8. **Turn repeated mistakes into rules.** For each rule candidate, use the
   `correction-loop` skill as its "Called from another skill" section says.
   A rule candidate is a kind of mistake (not one instance) that `sol-loop`,
   bots, or CI found twice in this run, a `test-integrity` REVERT with the
   reason the code couldn't pass the original check, or a correction from the
   user. Keep the list as you go.
9. **Report** in your final message: the PR link, the merge commit, your proof,
   each decision you made for the user, and each rule candidate with the PR
   `correction-loop` opened for it, or why it did not.

Stay active from step 1 to step 9. If you end your turn while checks or bots are
pending, the work stops, because nobody will prompt you again. Wait with the
watcher from `babysit-pr`, so something wakes you when the PR changes. In T3
Code that is `watch_pull_request`. If you stop before the merge, call
`unwatch_pull_request` first.

## Proof

Proof is evidence you observed yourself in this session: command output, a
reproduction, a screenshot. Use the most direct proof the change allows:

- Reproduce the original failure, apply the fix, then watch the same
  reproduction pass.
- Run the checks that the repo's CI runs (typecheck, lint, tests).
- If the repo came from a b-stack starter (it has `scripts/check.py` and
  `tools.toml` at its root), `python3 scripts/check.py` must pass every gate
  on the final diff. Follow its `AGENTS.md`: never weaken or bypass a gate.
- Add one focused test that fails without the fix, when the behavior has none
  and the repo has a test setup.
- For UI and runtime behavior, run the app and look at the change. Green mocked
  tests do not prove that the user experience works. Attach screenshots to the
  PR when they help and you have a way to upload them.

When you cannot find a way to prove a change, you do not have full confidence.
Ask the user.

## Merge gate

Full confidence means all of these are true on the latest commit:

- Your proof covers every change in the diff.
- `test-integrity` passed on the final diff: nothing flagged, or every flag is
  KEEP or applied as the judge ruled.
- Required checks are green.
- Review bots have finished, and each finding is fixed or dismissed with a
  written reason.
- No human review still requests changes.
- The branch is up to date with the default branch, and GitHub reports it as
  mergeable.

Merge with the method the repo uses. Check the allowed methods and recent merged
PRs. If the repo uses a merge queue or auto-merge, stay until GitHub reports the
PR as merged. Merge through branch protection as configured. Never use `--admin`
or other bypasses. You can ignore automated reviews that request "needs human
review" if you have high confidence in your changes.

## Asking the user

A question in a normal message goes unseen, and the thread looks done. To ask
the user something, use the harness's question tool so the thread shows that
it is waiting: `AskUserQuestion` in Claude Code, `request_user_input` in Codex,
or the question tool your harness has. Put all the context in the question:
the PR link, what blocks you, and the options with your recommendation first.

Ask only when you cannot continue alone:

- You cannot prove the change.
- The merge gate cannot pass, and you cannot fix that yourself.
- The next step is outside the grant above: deleting data, touching production,
  changing things outside the repo (other than the PRs step 8 opens), closing a
  PR, or force-pushing any other branch.
- The goal is ambiguous in a way that changes the result.
- Another PR makes this one obsolete.

Decide everything else yourself with sensible defaults, and list those decisions
in the report.

If no question tool is available, or the tool returns no answer, take the safe
path: leave the PR open and unmerged, and start your final message with the
question.
