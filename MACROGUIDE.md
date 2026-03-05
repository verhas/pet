<!-- ERROR executing code block: Snippet 'my_function' already exists in the file 'src/pet/AUTHORING_SKILL.md' -->
# PET Macro Authoring Guide

> **Version 1.0.2** · For the rationale behind PET see
> [RATIONALE.md](RATIONALE.md)

A *macro* is any `.py` file placed in the `.pet/` directory of your project.
When a template calls `use('name')`, PET executes that file in the template's
shared namespace, making everything it defines — functions, classes, constants —
available to the rest of the document.

This guide walks through every macro pattern used in PET's own library,
from the simplest single function to composable pipeline transformers.
All code examples are pulled live from `src/pet/macros`.

---

# 1 How `use()` Works

Before looking at patterns, it helps to understand exactly what `use()` does:

```python
<!-- ERROR executing code block: name 'dedoc' is not defined -->
```

That is all. PET reads the file as text and `exec`s it into the same namespace
that the rest of the template runs in. There is no import system, no module
registry, no special protocol. Everything the file defines at module level
becomes a name in the template.

Consequences:

- **Any valid Python is a macro.** Functions, classes, constants, imports,
  helper closures — whatever you `exec`, the template sees.
- **Names shadow each other.** If two macros define `helper`, the last one
  loaded wins. Use distinctive names or underscored private helpers.
- **Wildcards work.** `use('data/*')` loads every file matching
  `.pet/data/*.py`. Order is alphabetical.
- **Subdirectories work.** `use('data/yaml')` loads `.pet/data/yaml.py`.

---

# 2 Pattern 1 — The Pure Function

The simplest macro is a plain function. No class, no state, no setup.
Use this pattern when the operation is stateless: the same input always
produces the same output, and there is nothing to configure.

### `include.py`

```python
<!-- ERROR executing code block: name 'dedoc' is not defined -->
```

`include` is three lines of logic. It takes a filename, returns its content.
Templates use it as `{% doc | include('src/app.py') %}`.

### `dedent.py`

```python
<!-- ERROR executing code block: name 'dedoc' is not defined -->
```

`dedent` takes a string and returns a string. It is designed to compose with
`include`: the file being included may be indented inside a class or function,
and `dedent` strips the common prefix so the code block aligns to the left
margin in the output document.

**When to use a pure function:**

- The transformation has no parameters worth exposing
- There is no state to carry between calls
- The function is intended for composition (e.g. as a stage in a `pipe`)

---

# 3 Pattern 2 — The Callable Class

When the macro needs **configuration** set once at construction time, or needs
to **accumulate state** across multiple calls, use a class with `__call__`.

```python
<!-- ERROR executing code block: name 'dedoc' is not defined -->
```

The template creates an instance — `n = number(fmt="{:3d} ")` — and then
calls it — `{% doc | n(src('example')) %}`. Every call
advances the internal counter, so a second call continues numbering where the
first left off.

**The `__str__` convention:** if an object can end up on the right-hand side
of `doc |` but should not write anything visible (e.g. it is a container, not
a scalar value), implement `__str__` to return `''`. For `number`, the instance
itself is never passed to `doc |` — its *return value* is — so no `__str__`
is needed. For wrapper classes (see Pattern 4) it is essential.

**When to use a callable class:**

- Configuration that varies per use (`fmt`, `start`, `step`)
- Counter or accumulator state that persists across multiple calls in a template
- Any macro that is instantiated with `()` and then called with `()`

---

# 4 Pattern 3 — The Multi-Method Class

When the macro exposes several distinct operations, give them explicit names.
`__call__` handles the most common one; named methods handle the rest.

```python
<!-- ERROR executing code block: name 'dedoc' is not defined -->
```

In templates, `ch()` is the common case; `ch.open()` / `ch.close()` are used
when the document structure nests. The class name `chapter` is lowercase, which
matches the usage: `ch = chapter()` reads naturally.

**Class-naming convention:** PET uses lowercase class names throughout
(`chapter`, `number`, `yaml`, `pipe`). This lets the class name double as
its natural alias in templates — `ch = chapter()` rather than
`ch = Chapter()`. Follow this convention for consistency.

**When to use a multi-method class:**

- The macro has a clear primary operation (make it `__call__`) and secondary
  operations that are used less frequently
- The operations share state (the level stack in `chapter`)
- Named methods make the template more readable at the call site

---

# 5 Pattern 4 — The Data Reader

A data reader opens a structured file and exposes a navigation API.
PET ships with a shared base class, `_DataNode`, that handles dot-path
traversal and automatic wrapping of nested structures.

### The base class — `_node.py`

```python
<!-- ERROR executing code block: name 'dedoc' is not defined -->
```

`_DataNode` provides three things:

```
 1 get(path)   — navigate with dots; numeric segments index into lists
 2 __iter__   — iterate over list items or dict values
 3 __str__    — returns '' for dicts/lists, str(value) for scalars
```

### Extending the base — `yaml.py`

```python
<!-- ERROR executing code block: name 'dedoc' is not defined -->
```

The subclass does exactly two things: open the file and load it into
`self._data`. Everything else — `get()`, `__iter__`, `__str__`, wrapping
nested dicts in the same subclass — is inherited from `_DataNode`.

The same pattern is followed by `json.py` and `toml.py`. Create a new data
reader for any hierarchically structured format by inheriting `_DataNode`,
opening the file in `__init__`, and assigning the parsed result to
`self._data`.

### Flat formats — when not to use `_DataNode`

Some formats have dotted keys as first-class concepts.
A Java `.properties` file may contain the key `server.host` — the dot is
part of the key, not a path separator. Splitting on `.` would corrupt it.

For flat `key → value` formats, skip `_DataNode` and use a plain dict:

```python
<!-- ERROR executing code block: name 'dedoc' is not defined -->
```
do 1, 
**When to extend `_DataNode`:** hierarchical formats where dots in path
expressions are navigation, not key characters (YAML, JSON, TOML, XML).

**When to use a plain dict:** flat formats where dotted keys are literal
(`properties`, `.env`), or any format where you control the query API yourself.

---

# 6 Pattern 5 — The Pipeline Transformer

Some macros are not about data — they transform text. PET provides `pipe`
as a composable transformation primitive.

```python
<!-- ERROR executing code block: name 'dedoc' is not defined -->
```

Three design choices here are worth understanding before applying the pattern:

**The identity singleton.** `pipe` at the bottom of the file is a single
`Pipe()` instance with `_func = lambda x: x`. It is the starting point of
every pipeline. You never call `Pipe()` directly in a template; you start from
`pipe` and chain from there.

**The `_make` classmethod factory.** `__or__` and `and_then` need to create
new `Pipe` instances without going through the public constructor. `_make`
does this cleanly: it constructs a bare `Pipe` and injects the composed
function. The underscore signals that this is an internal factory; template
authors should not call it.

**`on_lines()`.** A transformation designed for a whole block (e.g. `dedent`)
may need to be applied line-by-line. `on_lines()` wraps any pipe stage into
a per-line mapper without changing the rest of the pipeline interface.

**When to use a pipeline macro:** when a transformation is better expressed as
a composition of smaller steps than as a single monolithic function, and when
callers will want to combine it with other transformations at the call site.

---

# 7 Writing Your First Macro

Here is a complete walkthrough. We will build `wordcount` — a macro that
counts words in a text block and keeps a running total across calls.

**Step 1 — Design the interface**

In the template, usage should read naturally:

```
{%
use('wordcount')
wc = wordcount()
%}

The introduction has {% doc | wc(intro_text) %} words.
The summary has {% doc | wc(summary_text) %} words.
Total: {% doc | wc.total %} words.
```

**Step 2 — Identify the pattern**

- Needs no file I/O → not a data reader
- Counts across calls → needs state → callable class (Pattern 2)
- One main operation (`__call__`) and one read-only attribute (`total`) →
  no secondary methods needed

**Step 3 — Implement**

```python
 4 class wordcount:
 5     def __init__(self):
 6         self.total = 0
 7
 8     def __call__(self, text):
 9         count = len(text.split())
10         self.total += count
11         return str(count)       # return a string — doc | can write it directly
12
13     def __str__(self):
14         return str(self.total)  # doc | wc writes the total
```

**Step 4 — Place the file**

Drop it in `.pet/wordcount.py`.  That is the whole installation step.
There is no registration, no `__init__.py`, no configuration file to update.

**Step 5 — Test it in a template**

```
{%
use('wordcount')
wc  = wordcount()
doc | wc("the quick brown fox") | " words in line 1\n"
doc | wc("jumps over the lazy dog") | " words in line 2\n"
doc | "total: " | wc.total | "\n"
%}
```

Output:

```
4 words in line 1
5 words in line 2
total: 9
```

---

# 8 Organising Macros in Subdirectories

As the library grows, group macros into subdirectories by category.
PET's own library uses `data/` for all file-format readers:

```
.pet/
    chapter.py
    number.py
    pipe.py
    data/
        yaml.py
        json.py
        toml.py
        xml.py
```

Load a macro from a subdirectory with a path-style name:

```python
use('data/yaml')      # loads .pet/data/yaml.py
use('data/*')         # loads all .py files directly under .pet/data/
use('**/*')           # loads everything, recursively
```

The path separator in `use()` is always `/`, regardless of platform.
PET uses `Path.glob()` internally, which handles the rest.

A macro in a subdirectory can import from a sibling file using a relative
path is **not** available — `use()` is `exec`, not `import`. Instead, share
common code by placing a helper module in the subdirectory and letting each
macro `exec` it:

```python
# .pet/data/myformat.py
exec(open('.pet/data/_shared.py').read())   # load shared helpers manually

class myformat:
    ...
```

Or, more cleanly, use a proper Python import if `pet-doc` is installed:

```python
# .pet/data/myformat.py
from pet.macros.data._node import _DataNode   # only works when package is installed

class myformat(_DataNode):
    ...
```

PET's own data macros use the latter approach, which is why `_node.py` starts
with an underscore — it is a library module, not a user-facing macro.

---

# 9 Quick Rules

```
1 Return strings — never print() at module level in a macro file.
2 Use doc | value or out(value) in templates to write to the document.
3 __str__ returns '' for container/wrapper objects, str(value) for scalars.
4 Name classes in lowercase so the class name works as a natural alias.
5 __call__ is the primary operation; named methods are secondary.
6 Configuration belongs in __init__; document output belongs in __call__.
7 State that persists between calls lives in instance variables.
8 Underscored names (_make, _DataNode, _wrap) are private to the library.
9 Place macros in .pet/; subdirectories are fine; no registration needed.
10 Use sys.exit() in a code block to turn a failed check into a build error.
```

---

*Generated from `MACROGUIDE.md.pet` by pet-doc
1.0.2 · `pet MACROGUIDE.md.pet MACROGUIDE.md`*
