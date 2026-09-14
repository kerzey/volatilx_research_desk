# Setting up the ChatGPT project

Two files, two different places.

1. **`PROJECT_INSTRUCTIONS.md`** — open it, copy everything below the horizontal rule, and paste it
   into the ChatGPT project's **Instructions** box.
2. **`RESEARCH_DESK_CONTEXT.md`** — upload the whole file to the project as a **project file**.

Name the project *VolatilX Research Desk*.

## What to paste in when you start a conversation

ChatGPT has no access to the desk, so give it whatever the conversation is about:

- **Discussing a verdict** — paste the report's Level 1 paragraph and the ledger row.
- **Discussing what to do next** — paste the "Waiting on you" section of `research/BOARD.md`.
- **Generating hypotheses** — paste the family you want to fill and the current backlog entries in
  it, so it does not re-propose something registered.
- **Discussing a platform defect** — paste the issue row and the relevant code lines. It cannot read
  the platform repo.

## Bringing the answers back

Whatever comes out goes into the desk the ordinary way:

- A hypothesis → append the `- [ ]` line to `research/INBOX.md`. The next desk cycle numbers it,
  files it in a family, and registers it ahead of everything else.
- An issue, enhancement or trade idea → paste the row into the matching file, or just describe it
  to the desk and let it file the row.

## Keeping it current

`RESEARCH_DESK_CONTEXT.md` has a date on it and §10 and §11 go stale as questions decide. Re-upload
it after any month in which a verdict lands. The parts that do not go stale are §3 through §9 — the
objective, the statistical frame, the lifecycle, the routing rules and the screen.

## One boundary

Never paste a credential, a connection string, a database URL or raw subscriber data into ChatGPT.
Nothing in the desk's process needs any of them, and the context file is written so that it does
not.
