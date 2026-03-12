---
name: pet-authoring
description: This skill should be used when the user wants to "write a pet template", "create a .pet file", "add snippet markers", "use a pet macro", "write a macro", "add line numbers", "include a file in a pet template", "read toml in pet", "read yaml in pet", "use pipe in pet", "number chapters in pet", or asks about pet template syntax, pet code blocks, pet expression syntax, {{ }} blocks, or how to author pet documents. Also applies whenever editing any file that may have a corresponding .pet source template — always check for a .pet counterpart before modifying a generated output file.
version: 1.0.0
---

# PET — Template & Macro Authoring

## CRITICAL RULE — Never Edit Generated Files

If a file `X` exists alongside a corresponding `X.pet` template (e.g. `README.md`
and `README.md.pet`), **never modify `X` directly**. It is a generated output and
any edits will be overwritten the next time the template is processed.

Always edit the `.pet` source instead, then regenerate:

```bash
pet README.md.pet README.md
```

This rule applies to every file format — `.md`, `.txt`, `.html`, `.adoc`, or any
other extension. If `X.pet` exists, `X` is owned by PET.

Reference for writing `.md.pet` templates and macros for the `pet-doc` tool.

---

## Template Syntax

A `.md.pet` file is plain text with two kinds of Python blocks:

| Syntax | Purpose |
|--------|---------|
| `{% statements %}` | Execute Python — output via `print`, `doc \|`, or `out()` |
| `{{ expr }}` | Evaluate an expression and write its value directly |

`{{ expr }}` is the preferred shorthand for single values — no `doc |` needed:

```
{{ VERSION }}
{{ ch() }} Introduction
{{ n(src('main_loop')) }}
```

Multi-statement setup blocks still use `{% %}`:

```
{%
use('chapter')
ch = chapter()
%}
```

To write the PET delimiters literally inside a code block (e.g. to document PET itself),
build them with string concatenation to avoid confusing the processor:

```python
OB = '{' + '%'   # {%
CB = '%' + '}'   # %}
OE = '{' + '{'   # {{
CE = '}' + '}'   # }}
```

Then use `{{ OB }}`, `{{ CB }}`, `{{ OE }}`, `{{ CE }}` in the template body.

---

## Writing to the Document

**Always prefer `{{ expr }}`** — it is the clearest and most concise form:

```
{{ VERSION }}
{{ ch() }} Introduction
{{ n(dedent(include('src/core.py'))) }}
```

Only reach for `doc |` or `out()` when `{{ }}` cannot express what you need:

| Situation | Use instead | Example |
|-----------|-------------|---------|
| Writing multiple values in sequence without newlines | `doc \|` | `doc \| prefix \| value \| suffix` |
| Output with no trailing newline, mid-statement | `out(value)` | `out("• ")` inside a loop |
| Chaining transformations inline with side effects | `doc \|` | `doc \| ch() \| " " \| title` |

The full set of output mechanisms:

| Expression | Effect |
|---|---|
| `{{ expr }}` | **Preferred.** Evaluates expression, writes `str(result)` |
| `doc \| value` | Writes `str(value)`; chainable: `doc \| a \| b \| c` |
| `out(value)` | Writes `str(value)` without a trailing newline |

`doc` is a `_Doc` instance injected into every template's namespace by the processor.
Container/wrapper macros (data readers, `snippet`) implement `__str__` returning `''`
so they are safe to accidentally pass to `doc |` without emitting anything.

---

## Loading Macros with `use()`

`use('name')` executes `.pet/name.py` in the template's shared namespace.
Everything that file defines at module level becomes available immediately.

```python
use('chapter')          # loads .pet/chapter.py
use('data/yaml')        # loads .pet/data/yaml.py
use('data/*')           # loads all .py files directly under .pet/data/
use('**/*')             # loads everything recursively
```

- Order is alphabetical within a glob.
- Names shadow each other — if two macros define `helper`, the last one loaded wins.
- `use()` is `exec`, not `import` — standard relative imports do not work inside macro files.

---

## Built-in Macros — Quick Reference

### chapter — section numbering

```python
use('chapter')
ch = chapter()          # default: "#" prefix, " " separator

{{ ch() }}        # emits "# 1", "# 2", …
{{ ch.open() }}   # push a level: "## 1.1", "### 1.1.1", …
{{ ch.close() }}  # pop a level
```

Constructor options: `chapter(header_prefix="#", sep=" ")`

### number — line numbering

```python
use('number')
n = number(fmt="{:3d}  ")   # configure once

{{ n(some_text) }}    # prefixes each line with a counter
```

Constructor options: `number(start=1, step=1, fmt="{} ")`
Counter persists across calls — useful for numbering a whole document sequentially.

### include — file inclusion

```python
use('include')
{{ include('src/app.py') }}
```

Returns the file contents as a string. Compose with `dedent` and `number`:

```python
{{ n(dedent(include('src/app.py'))) }}
```

### dedent — strip indentation

```python
use('dedent')
{{ dedent(include('src/nested.py')) }}
```

Removes the common leading whitespace from all lines and strips trailing
whitespace per line.

### snippet — extract named code blocks

The first argument (`source`) can be a directory, a glob pattern, or a list of either:

```python
use('snippet')
src = snippet('src/')                          # scan a directory recursively
src = snippet('src/**/*.py')                   # glob — only Python files
src = snippet(['src/**/*.py', 'lib/**/*.py'])  # list of globs
src = snippet(['src/', 'tests/'])              # list of directories
```

Use `exclude` to skip files that would cause false positives (e.g. documentation
files whose prose accidentally matches the snippet marker regex):

```python
src = snippet('src/', exclude='*.md')               # single glob
src = snippet('src/', exclude=['*.md', '*.adoc'])   # multiple globs
```

Emit a named snippet:

```python
{{ src('my_function') }}
```

A glob that matches no files is not an error — it simply contributes no snippets.

See the **Snippet Markers** section below for how to annotate source files.

### Data readers

All hierarchical readers expose `get("dot.separated.path")`.
Lists support integer indices: `get("dependencies.0.name")`.
`str(reader)` returns `''` (use `.get()` to extract values).

```python
use('data/toml')
proj    = toml("pyproject.toml")
version = proj.get('project.version')   # "1.0.2"

use('data/yaml')
cfg = yaml("config.yaml")
host = cfg.get('server.host')

use('data/json')    # identical API to yaml
use('data/xml')     # xpath-style path; cfg.attr('attrname') for attributes
use('data/properties')   # flat key=value; dotted keys are literal, not paths
use('data/env')     # .env files; strips quotes, skips comments
```

### pipe — composable transformations

```python
use('pipe')
use('dedent')
use('number')

n     = number(fmt="{:3d}  ")
clean = pipe | dedent | n          # chain with |

{{ clean(include('src/core.py')) }}
```

Apply a stage line-by-line with `.on_lines()`:

```python
shout = pipe | str.upper
{{ shout.on_lines()(include('words.txt')) }}
```

---

## Snippet Markers

`snippet(directory)` scans source files for start/end marker comments.
The regex matches any line containing `snippet <identifier>` (case-insensitive)
for the start, and `end snippet` for the end.

Add markers in the comment style of each language:

### Python
```python
# snippet my_function
def my_function(x):
    return x * 2
# end snippet
```

### Java / C / C++ / Go / JavaScript / TypeScript
```java
// snippet my_function
public int myFunction(int x) {
    return x * 2;
}
// end snippet
```

### Shell / Ruby / YAML / TOML
```bash
# snippet deploy_step
docker build -t myapp .
docker push myapp
# end snippet
```

### HTML / XML
```html
<!-- snippet nav_bar -->
<nav>...</nav>
<!-- end snippet -->
```

### SQL
```sql
-- snippet get_users
SELECT * FROM users WHERE active = 1;
-- end snippet
```

**Gotcha — false positives:** The regex is broad. Any line matching
`snippet <word>` anywhere in the file will be treated as a start marker —
including docstrings. Keep docstrings in macro files free of the literal
phrase `snippet <word>` (rephrase, or quote the word).

---

## Common Template Patterns

### Version badge from pyproject.toml

```python
{%
use('data/toml')
proj    = toml("pyproject.toml")
VERSION = proj.get('project.version')
%}
Version: {{ VERSION }}
```

### Auto-numbered chapters

```python
{%
use('chapter')
ch = chapter()
%}
{{ ch() }} Introduction
{{ ch() }} Installation
{{ ch() }} Usage
```

Outputs: `# 1 Introduction`, `# 2 Installation`, `# 3 Usage`.

### Numbered code listing from source

```python
{%
use('include')
use('dedent')
use('number')
n = number(fmt="{:3d}  ")
%}
{{ n(dedent(include('src/core.py'))) }}
```

### Embed a named snippet with line numbers

```python
{%
use('snippet')
use('number')
src = snippet('src/**/*.py')   # glob to select only Python files
n   = number(fmt="{:3d}  ")
%}
{{ n(src('main_loop')) }}
```

### Build error on missing value

```python
{%
use('data/toml')
import sys
proj = toml("pyproject.toml")
if not proj.get('project.version'):
    sys.exit("ERROR: version missing from pyproject.toml")
%}
```

---

## Writing a Custom Macro

Place a `.py` file in `.pet/`. No registration needed — `use('name')` finds it.

**Pattern 1 — Pure function** (stateless, no configuration):
```python
def shorten(text, max_len=80):
    return text[:max_len] + '…' if len(text) > max_len else text
```

**Pattern 2 — Callable class** (configuration + optional state):
```python
class wordcount:
    def __init__(self):
        self.total = 0

    def __call__(self, text):
        count = len(text.split())
        self.total += count
        return str(count)

    def __str__(self):
        return str(self.total)   # doc | wc writes the running total
```

**Key conventions:**
- Class names are **lowercase** (`chapter`, `number`, `yaml`) so the class name works as its natural alias: `ch = chapter()`
- `__str__` returns `''` for container/wrapper objects; `str(value)` for scalars
- Macros **return strings**; they never `print()` at module level
- `__call__` is the primary operation; named methods are secondary
