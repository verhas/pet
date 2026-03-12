---
name: pet
description: This skill should be used when the user wants to "install pet", "run pet", "process a pet template", "render a .pet file", "watch a pet template", "regenerate all pet templates", "initialise pet", "force reinitialise pet", "install pet skill for Claude", or asks about the pet tool. Provides guidance for all pet CLI commands.
version: 1.0.0
---

# PET — Program Enhanced Text

Skills for installing and running `pet`, a Python documentation automation tool.
Templates are `.md.pet` files with two kinds of Python blocks:

- `{% ... %}` — execute statements; output via `print`, `doc |`, or `out()`
- `{{ expr }}` — evaluate an expression and write its value directly (Jinja2-style)

---

## pet-install

**Trigger:** user wants to install pet or run pet for the first time

Install `pet` from PyPI:

```bash
pip install pet-doc
```

Using a virtual environment is recommended — it isolates `pet` from other Python
tools on the system, avoids permission issues, and is especially important when
commands are executed by an LLM on the user's behalf (where a clean, predictable
environment prevents unintended side effects):

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install pet-doc
```

When running subsequent `pet` commands on behalf of the user, always activate
the virtualenv first or invoke pet via `.venv/bin/pet` directly.

Then verify the installation:

```bash
pet --help
```

---

## pet-init

**Trigger:** user wants to initialise, reinitialise, or force-reinitialise the `.pet/` macro directory

Run from the project root:

```bash
pet init                  # first-time setup; safe to re-run
pet init -f               # force regeneration, ignoring local edits
pet init for_claude       # also installs the pet skill into Claude Code (.claude/)
pet init -f for_claude    # force + Claude skill install
```

Behaviour of `pet init`:
- No `.pet/` → creates it and writes a `.hash` checksum of the installed macros.
- `.pet/` exists, hash matches → macros untouched; regenerates with the latest version.
- `.pet/` exists, hash differs → local edits detected; skips (use `-f` to override).
- `.pet/` exists, no `.hash` → created by an older version of pet; skips (use `-f` to override).

`for_claude` copies the pet skills into `.claude/skills/` in the current project
so Claude Code can offer context-aware help for pet commands.

---

## pet-process

**Trigger:** user wants to process / render / regenerate a `.pet` template file

Usage pattern: `pet <input.md.pet> <output.md>`

Common invocations:

```bash
pet README.md.pet README.md
pet MACROGUIDE.md.pet MACROGUIDE.md
pet RATIONALE.md.pet RATIONALE.md
```

Explicit subcommand form (equivalent):

```bash
pet process <input.md.pet> <output.md>
```

When asked to "regenerate" or "render" a doc, find the corresponding `.md.pet` source
and run the appropriate command above. If the output file is not specified, derive it
by stripping the `.pet` suffix from the input.

---

## pet-errors

**Trigger:** a `pet` command exits with an error

When `pet` fails, read the error message carefully before taking any action.

**Consistency check failures** are the most common cause. They look like:

```
CONSISTENCY FAILURE in RATIONALE.md.pet
  pyproject.toml version : 1.0.2
  _stated_version        : 1.0.0
Update _stated_version to match the release, or bump pyproject.toml.
```

A consistency check is a deliberate guard written into the template by the
document author to prevent the documentation from silently drifting out of sync
with the codebase. It failing means the template and the project data disagree —
this is not a bug in `pet`, it is the system working as intended.

**When a consistency check fails:**

1. Read the error message and identify exactly which values disagree.
2. Apply the `pet-authoring` skill to understand the template structure.
3. Present the conflict and the proposed fix to the user clearly.
4. **Wait for explicit human approval before making any edit to the `.pet` file.**

Never silently update a consistency check value, version number, or any other
fact in a `.pet` template without the user reviewing and confirming the change.
The check exists precisely because such changes carry meaning — they assert
something about the state of the project — and that assertion must be validated
by a human, not inferred by an LLM.

---

## pet-watch

**Trigger:** user wants to watch a template and auto-regenerate it on every save

```bash
pet watch <input.md.pet> <output.md>
```

Optional polling interval (default 0.5 s):

```bash
pet watch <input.md.pet> <output.md> --interval 1.0
```

Press Ctrl+C to stop watching. This command blocks the terminal, so inform the user
it will run until interrupted.

---

## pet-all

**Trigger:** user wants to regenerate all `.pet` templates in the project

Find every `*.md.pet` file and process each one:

```bash
for f in $(find . -name "*.md.pet" -not -path "./.venv/*"); do
    out="${f%.pet}"
    echo "Processing $f -> $out"
    pet "$f" "$out"
done
```

List the files that will be processed before running, so the user can confirm.
