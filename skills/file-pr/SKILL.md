---
name: file-pr
description: File a concise pull request. Use when the user asks to file, open, or create a PR.
---

# File PR

Before filing, check whether a PR for this branch already exists. Review the
diff locally against the base branch (usually `origin/main`) to make sure its
contents match the goal.

PR titles usually become commit messages, so follow the repository's title
conventions. Look at recently merged PRs and Git history for examples. Prefer a
concise, human-readable title that explains why the change matters:

BAD

> ❌ perf(server): negotiate permessage-deflate on the websocket

GOOD

> ✅ perf(server): cut websocket frame size by 70%+ with gzipping

Open the description with a simple explanation of the problem based on the
user's original prompt, then briefly explain the solution. Do not lead with an
implementation inventory:

BAD

> ❌ Removed implicit workspace carry-over from every "new thread" entry point (cmd+n / cmd+shift+o, sidebar v1/v2 buttons, command palette). New threads inherit only the project from context; branch, worktree, and env mode always come from the configured defaults. Deleted buildContextualThreadOptions, startNewThreadInProjectFromContext, and the v1 sidebar's seed-context machinery.

GOOD

> ✅ My "new worktree" default was ignored when starting new threads on existing worktrees. Super unintuitive. Now your preferences always apply.

## Write for a colleague without prior context

Assume the reviewer is an engineer who has not followed the task or worked on
this part of the application. Briefly explain the affected user experience or
system responsibility before naming internal components. Introduce unfamiliar
terms by role, then name/link the implementation. Explain before/after behavior
and why the change matters; do not require the chat, ticket history, or another
PR to understand the description. Avoid both unexplained app vocabulary and
basic programming tutorials.

## Consistent description layout

Use GitHub Markdown with short paragraphs, clear heading hierarchy, and blank
lines around lists and code fences. For substantive changes, use this order:

- `## Summary`: the problem, relevant context, and resulting behavior.
- `## How it works`: an optional, compact overview showing how the pieces connect.
  Keep it only when it adds context beyond the individual review stops.
- `## Review guide`: numbered `###` stops in the order that makes the change
  easiest to understand, rather than commit or filename order. Each stop explains
  the component's role, the behavior that changed, and links the relevant code.
  Each stop addresses a distinct review question or area of the change. Place a
  focused diagram beside that stop when it clarifies its behavior or contract;
  do not gather all diagrams at the top. Add a specific **Review focus** or
  **Tradeoff** only when it warrants attention.
- `## Validation`: checks actually run, their outcomes, and material limits.
  Distinguish fresh checks from historical evidence; never imply an unrun check
  passed. Use a compact table when several independent checks need comparison.

Scale the layout to the diff: a small change can use a short summary and
validation paragraph. Avoid empty sections, repeated summaries, exhaustive file
inventories, and boilerplate review questions. Keep sample-only notices obvious
but separate from the explanation of the actual change. Close with attribution.

## Mermaid diagrams

Diagrams are expected wherever they help the reviewer see the change: meaningful
branching, data movement, asynchronous behavior, component boundaries, gates or
pipelines, or state transitions. In a substantive change, a review stop about one
of these should usually have its own diagram beside it. Explaining such a flow in
prose alone, when a diagram would show it at a glance, is a defect. Do not force a
diagram into a trivial change, or onto a stop that is only a rename, a config
value, or a list. Use separate focused diagrams only when each answers a
different review question.

Use a consistent visual grammar in fenced `mermaid` blocks:

- Default to `flowchart TD`; use `LR` when a short linear pipeline reads better.
- Use rounded nodes for entry/end points, rectangles for operations, and diamonds
  for decisions. Label decision edges, such as Yes/No, with concise conditions.
- Use short, quoted, plain-language labels. Explain app-specific names in nearby
  prose; do not make the diagram a graph of unexplained symbols.
- Use the pstack statechart **Subtle** pastel palette with dark node text and
  restrained borders. Keep color meanings consistent across the PR: blue for
  inputs, lavender for decisions/processing, peach for waiting or retained state,
  teal for applied results, and pink for errors. Labels must convey the meaning
  without relying on color. Define only the classes used in each diagram.
- Embed explicit Mermaid `classDef` styles so the palette renders in GitHub:
  `input fill:#c3e0ff,stroke:#808080,color:#1c1c1c`,
  `decision fill:#e3d5ff,stroke:#808080,color:#1c1c1c`,
  `retained fill:#f0d3bf,stroke:#808080,color:#1c1c1c`,
  `result fill:#bfe3df,stroke:#808080,color:#1c1c1c`, and
  `error fill:#ffcbe6,stroke:#808080,color:#1c1c1c`.
  Apply classes to node IDs with `class A,B input`, for example. Processing nodes
  can use the same lavender style as decisions while keeping rectangular shapes.
- Keep the shape grammar consistent. Choose direction per diagram for readability:
  a compact overview may use LR while branching review details use TD. Do not add
  custom zoom/pan controls, icons, HTML labels, or decorative wrappers. Host-provided
  viewer controls are outside the PR body's control.
- Trace branches and ordering against the actual code. Include relevant failure,
  stale-response, or cancellation paths when they affect the change. Distinguish
  a conceptual overview from an exhaustive state machine or formal proof.

Check Mermaid syntax with an available parser/renderer when practical. Before
publishing, check the diagram's meaning against the code and confirm that all
file/line links resolve at the reviewed revision. The PR body must contain the
actual Mermaid source so GitHub can render it, not only an image or external link.

## Mobile verification evidence is a filing requirement

For changes that affect mobile behavior, required verification evidence must
exist and be reviewable before opening a PR, including a draft. Missing,
failing, incomplete, or inaccessible evidence means the affected work is
unfinished: complete implementation and verification first. Do not file with
promised recordings, evidence placeholders, or required flows marked NOT_RUN
or BLOCKED. If verification cannot proceed, report the concrete blocker and
leave the work unfiled. Pure documentation/tooling changes with no mobile
behavior impact do not require fabricated app recordings.

### Cover the full affected journeys

Trace the diff's blast radius through user journeys, including shared state,
navigation, data loading, lifecycle behavior and downstream surfaces such as
widgets when affected. Identify every affected flow and relevant changed branch
before checking evidence. A recording of the edited screen alone is insufficient
when the change can affect earlier steps or later outcomes.

Provide a separate, clearly named video for each affected flow. Start recording
at the flow's real entry point with enough setup to understand the initial state;
perform the real user actions; continue through the final observable outcome and
any affected downstream behavior. Show relevant loading, error/recovery,
interruption, persistence or return paths when those are part of the change.
Separate scenario videos are appropriate when branches cannot be demonstrated
clearly in one continuous run. Avoid cuts that hide the transition or outcome
being verified; screenshots supplement video, never replace required flow video.

Use evidence from the actual app build under review. Record the tested source
revision, build identifier or artifact hash, device/OS, runner and fixture/test
conditions. Existing evidence is reusable only when it covers the complete
current blast radius on the applicable build. Code changes that affect a recorded
flow invalidate that flow's evidence until rerun; do not relabel an older video
as a fresh verification result. Historical/sample evidence is not current proof.

### Prefer Revyl; fall back to the local emulator

Use Revyl whenever it can execute and record the required mobile flows. Read
available Revyl skill/project instructions when operating it. If Revyl is
unavailable or encounters an infrastructure, installation, execution or recording
problem that prevents verification, use the authorized local emulator and
capture equivalent end-to-end evidence. Note the concrete Revyl problem and
which flows were verified locally. Preserve coverage and acceptance criteria
across runners. An application assertion failure is a product finding to
investigate/fix, not a reason to switch runners to obtain a pass. If neither
runner can provide the required evidence, keep the work unfiled.

### Choose evidence that lets the reviewer judge the change

Use visuals only where they answer a concrete review question about what the
user sees. Do not add a screenshot or recording to every review stop. Internal
logic, contracts and code structure usually need an explanation, diagram or test
result; do not invent UI evidence for them. Keep supporting regression recordings
in the evidence index instead of repeating them throughout the guide.

Match the medium to the claim:

- Animation, scene transitions, gestures, loading continuity and other behavior
  over time require playable video showing the action and result at normal speed.
  A final-state screenshot, contact sheet, diagram or telemetry cannot establish
  how the transition looks. Tell the reviewer what to watch for in the recording;
  add useful timestamps when known, without inventing them. Do not claim visual
  acceptance from automation alone; watch the relevant playback before grading it.
- Static appearance and visible bug comparisons use screenshots at the relevant
  checkpoint. Include motion video as well when timing or interaction causes the
  bug. Do not use a screenshot as the sole evidence for an animation fix.
- A clickable screenshot is only a video thumbnail. Label it **Play recording**
  and make the destination clear; the linked recording supplies motion evidence.
  The label text must itself be a link to the same recording, e.g.
  `[![Play recording](thumb.png)](video.mp4) [**Play recording**](video.mp4)`.
  Never leave it as plain bold text: thumbnails from a private repo do not load
  in the GitHub mobile app, emails or logged-out views, and then the text link is
  the only way in. Use one representative thumbnail where helpful, not one for
  every assertion.

Retain required end-to-end flow coverage, but present each item once where it is
most useful. More attachments do not substitute for evidence of the stated claim.

### Attach evidence where the reviewer needs it

For Revyl runs, reuse Revyl's existing recording: link directly to its recording
or report and embed a representative screenshot as a clickable thumbnail that
opens that recording/report. Do not separately record, download or re-upload the
same Revyl video. Confirm the report includes a playable recording and reviewers
can access it. Use a clear caption identifying the flow and its outcome.

For local-emulator fallback runs, attach the recorded flow videos or link durable,
reviewer-accessible video artifacts. Local fallback videos must still cover each
flow from entry through outcome. A local filesystem path, inaccessible report or
test log without its recording does not satisfy this requirement. Prepare
reviewer-accessible artifacts before filing so the PR starts with complete
evidence; use supported upload/artifact mechanisms rather than inventing URLs.
If the videos can only go on an evidence branch, link each with
`https://github.com/<owner>/<repo>/blob/<branch>/<file>.mp4?raw=true` so it opens
the video file rather than GitHub's file page, which in a private repo may not
play it. Say in the Evidence note that the owner can drag the files into the
description for inline playback.
Check that each linked recording exists, plays, and shows the complete claimed
flow. Use authorized test data and check recordings for secrets/private details.

Place each video beside its relevant review stop, with a short caption explaining
the starting state, actions and expected/observed outcome. For multiple flows,
add a compact evidence index under Validation mapping each flow/scenario to its
recording, result, runner/device and tested build. Make uncovered required flows
visible during preparation and resolve them before filing; unrelated deferred
features must not be presented as verified. Only after all required flows pass
and the evidence is accessible is the mobile change ready to become a PR.

## Bug-fix comparisons

For bug fixes with a visible symptom, include a side-by-side before/after screenshot comparison
beside the relevant review stop. The left panel shows the reproduced bug on the
unfixed build, with a red outline around the specific defect and a concise
annotation explaining it. The right panel shows the fixed result. Label the
panels **Before — bug** and **After — fixed**. Use two separate image files in a two-column table with independent labels and visible layout spacing between them (a narrow empty spacer column is appropriate). Keep the red outline and annotation on the before image only. Do not combine the captures into one image or bake a white strip into an image to simulate spacing. Identify both source revisions or
builds and preserve the original unannotated captures.

Match device, viewport, scale, theme, fixture data, starting state and interaction
checkpoint wherever possible so the comparison isolates the fix. Explain any
unavoidable difference. Keep the full relevant UI visible; annotations must not
obscure the defect. Do not synthesize a before state or present another app/build
as a reproduction. If the bug depends on timing or interaction, include the
required flow recording as well; still images do not establish a behavioral fix.
For Revyl captures, keep the clickable recording/report link with the comparison.
Missing real before/after evidence is an unfinished verification item, not a
placeholder to publish. Use separate images in a side-by-side table that remains legible in the PR;
attach or link the originals for closer inspection.

## Publish

End the description with the public model name and harness that made the
changes, for example `Created with <model> in <harness>.` Include subagent
models that wrote part of the change. Use the model name the harness reports.
If model identity is unavailable, name the harness without guessing a model.

Before submission, check the title, description, quotes, and attachments for
secrets and private details.

After applicable verification and evidence requirements are satisfied, open a
real PR rather than a draft so review bots run. If `gh pr create` fails
because the GraphQL rate limit is used up, open it through REST with
`gh api repos/<owner>/<repo>/pulls -f title=... -f head=... -f base=... -F body=@<file>`. If the user also asked
to babysit it, continue with the `babysit-pr` skill.

Do not post a follow-up PR comment unless it serves the user's request. When a
comment is needed, use the `leaving-pr-comments` skill.
