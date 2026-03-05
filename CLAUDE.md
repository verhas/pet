# PET — Claude Code Session Notes

## Project

**pet-doc** — Program Enhanced Text, a Python documentation automation tool.
Templates are `.md.pet` files containing `{% ... %}` Python code blocks; PET
executes them and splices the output into the final document.

- Repo: https://github.com/verhasp/pet
- PyPI: `pet-doc` (published, current release 1.0.1; local version is 1.0.2
  with `license = "Apache-2.0"` fix, not yet published)
- Python 3.11+, build backend: Hatchling

## Key Conventions

- **Lowercase class names** throughout the macro library (`chapter`, `number`,
  `snippet`, `pipe`, `yaml`, `toml`, …). The class name doubles as its natural
  alias in templates: `ch = chapter()`.
- **`__str__` returns `''`** for container/wrapper objects (e.g. data readers,
  `snippet`); returns the value as a string for scalars.
- **`doc | value`** writes `str(value)` to the document. `doc` is a `_Doc`
  instance defined in `processor.py`.
- **`use('name')`** execs `.pet/name.py` into the template namespace.
  Wildcards and subdirectories work: `use('data/*')`, `use('data/yaml')`.
- **`OB = '{' + '%'`** / **`CB = '%' + '}'`** — required trick to write the
  PET delimiters literally inside a `{% %}` block (direct `%}` would close it).

## Project Structure

```
src/pet/
    cli.py              # 'pet' entry point: init / process / watch
    processor.py        # template engine; defines doc, use(), out()
    macros/             # installed macro library (copied to .pet/ on init)
        chapter.py      # chapter counter class
        number.py       # line-numbering class
        include.py      # include(filename) pure function
        dedent.py       # dedent(text) pure function
        snippet.py      # snippet(directory) — scans for marked code blocks
        pipe.py         # pipe pipeline transformer
        data/
            _node.py    # _DataNode base class for hierarchical data readers
            toml.py yaml.py json.py xml.py properties.py env.py

.pet/                   # project-local macro library (mirrors src/pet/macros/)
    (same structure as src/pet/macros/)

tests/
    test_chapter.py  test_snippet.py  test_env.py  test_properties.py
    test_yaml.py  test_json.py  test_toml.py  test_xml.py  test_pipe.py
    test_number.py  test_include.py  test_dedent.py  test_processor.py
    test_cli.py  test_watch.py  test_chapter_template.py
    chapter/            # golden-file test for chapter template
    snippet/            # fixture files for snippet tests
    env/ toml/ yaml/ json/ xml/ properties/   # fixture files

RATIONALE.md.pet / RATIONALE.md        # theory doc (single-source-of-truth, LLM/RAG)
MACROGUIDE.md.pet / MACROGUIDE.md      # macro authoring guide (patterns 1–5)
README.md.pet / README.md              # project README
```

## Snippet Macro — Important Notes

- Start marker: any line matching `snippet\s+[identifier]` (case-insensitive)
- End marker: any line matching `end\s+snippet` (case-insensitive)
- The regex is broad — **docstrings containing "snippet <word>" are false
  positives**. Keep docstrings in `snippet.py` free of this pattern (use
  quotes: `'snippet'` or rephrase).
- `snippet.md` was deleted from `src/pet/macros/` — it caused false positives.
- The `use_function` snippet is marked in `processor.py` (lines ~48–72) and
  pulled into MACROGUIDE via `src('use_function')`.

## MACROGUIDE.md.pet — `dedoc` function

Defined in the preamble, strips docstrings from included source before
displaying in the guide:

```python
def dedoc(lines):
    on = True
    ret = ""
    for line in lines.split("\n"):
        if line.strip() == '"""':
            on = not on
            continue
        if on:
            ret += line + "\n"
    return ret
```

Used as: `{%doc | dedoc(dedent(include(MACRO_DIR + '/data/yaml.py')))%}`

## Current State

- **All tests pass** when running inside the project `.venv` (which has all
  dependencies installed). Always use `source .venv/bin/activate` before
  running `pytest`; the system Python lacks `pyyaml`.
- `pyproject.toml` has `version = "1.0.2"` and `license = "Apache-2.0"` —
  **not yet committed or published**.
- `MACROGUIDE.md` needs to be regenerated after the `dedoc` bug fixes.
- The `.pet/` directory and `.idea/` are untracked (not in `.gitignore` yet).

## Running PET

```bash
# Process a template (from project root)
python3 -c "from src.pet.processor import process_template; process_template('X.md.pet', 'X.md')"

# Or install in dev mode first, then use the CLI directly
pip install -e .
pet README.md.pet README.md
pet MACROGUIDE.md.pet MACROGUIDE.md
```

## Publishing

```bash
hatch build
python -m twine upload dist/pet_doc-1.0.2*   # uses ~/.pypirc with __token__
```

## Open Items

- Regenerate MACROGUIDE.md with the fixed `dedoc` function
- Commit the current working changes (pyproject.toml version/license, snippet
  rename, README format note, MACROGUIDE dedoc fixes)
- Publish 1.0.2 once the above are done
- `.pet/` should probably be added to `.gitignore` (it is a project-local
  runtime directory, not source)
