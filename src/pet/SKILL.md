---
name: pet
description: This skill should be used when the user wants to "install pet", "run pet", "process a pet template", "render a .pet file", "watch a pet template", "regenerate all pet templates", "initialise pet", or asks about the pet-doc tool. Provides guidance for all pet CLI commands.
version: 1.0.0
---

# PET — Program Enhanced Text

Skills for installing and running `pet-doc`, a Python documentation automation tool.
Templates are `.md.pet` files; `{% ... %}` blocks are executed and their output is
spliced into the output document.

---

## pet-install

**Trigger:** user wants to install pet, set up the dev environment, or run pet for the first time

Install `pet-doc` in editable (development) mode into the project virtualenv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

Then verify the installation:

```bash
pet --help
```

If `.venv` already exists, skip virtualenv creation and just activate + install.

---

## pet-init

**Trigger:** user wants to initialise the `.pet/` macro directory in a project

Run from the project root:

```bash
pet init
```

This copies the built-in macro library into `.pet/` so templates can call `use('...')`.
Only needed once per project. If `.pet/` already exists, `pet init` is a no-op.

To also register the pet skill with Claude Code:

```bash
pet init for_claude
```

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
