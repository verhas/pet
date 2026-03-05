# PET — Program Enhanced Text: Reference for LLMs

This document tells you everything you need to generate valid PET templates.
PET is a lightweight documentation automation tool: it processes `.pet` template
files and produces plain text output (most commonly Markdown, but any format works).

---

## 1. What is a PET template?

A PET template is any text file that contains `{%` ... `%}` blocks.
Everything outside those blocks is copied verbatim to the output.
Everything inside a block is executed as Python code in a shared namespace.

The output file is typically named after the template without the `.pet` extension:

```
README.md.pet  →  README.md
docs.adoc.pet  →  docs.adoc
```

PET is **not Markdown-specific**. The template extension and output format are
entirely up to you. Markdown is the most common use case.

---

## 2. Block syntax

### Setup block (no output)

```
{%
use('chapter')
use('number')
ch = chapter()
n  = number(fmt="{:3d}  ")
%}
```

A block whose code does not call `doc |` produces no output.
Use setup blocks at the top of the template to load macros and define variables.

### Inline output block

```
{% doc | VERSION %}
```

`doc | value` writes `str(value)` into the document at that position.
Multiple values can be chained: `doc | "v" | VERSION | "\n"`.

### Multi-value inline block

```
{% doc | ch() %} Introduction
```

The `ch()` call returns the next chapter heading prefix (`# 1`, `## 1.1`, etc.)
and `doc |` inserts it before the literal text that follows on the same line.

---

## 3. The `doc` object and pipe operator

`doc` is the output sink for the current template.
`doc | value` appends `str(value)` to the document and **returns `doc`**, so
you can chain: `doc | "foo" | "bar" | "\n"`.

`doc | value` is the only way to produce output from a `{% %}` block.
Anything printed with `print()` goes to stderr, not the document.

---

## 4. Loading macros — `use()`

```python
use('chapter')           # loads .pet/chapter.py
use('number')            # loads .pet/number.py
use('snippet')           # loads .pet/snippet.py
use('include')           # loads .pet/include.py
use('dedent')            # loads .pet/dedent.py
use('pipe')              # loads .pet/pipe.py
use('data/toml')         # loads .pet/data/toml.py
use('data/yaml')         # loads .pet/data/yaml.py
use('data/json')         # loads .pet/data/json.py
use('data/xml')          # loads .pet/data/xml.py
use('data/properties')   # loads .pet/data/properties.py
use('data/env')          # loads .pet/data/env.py
```

`use()` executes the named `.py` file into the template's shared namespace.
Each call makes the macro's class or function available by its lowercase name.
You can also use glob patterns: `use('data/*')` loads all data macros.

---

## 5. Macro reference

### 5.1 `chapter` — hierarchical section counter

```python
use('chapter')
ch = chapter(header_prefix="#", sep=" ")
```

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `header_prefix` | `"#"` | Markdown heading character(s) |
| `sep` | `" "` | Separator between `#` symbols and the counter |

**Usage:**

```
{%doc | ch()%} Introduction          # -> # 1 Introduction
{%doc | ch()%} Getting Started       # -> # 2 Getting Started
```

Auto-numbering increments at the depth of `header_prefix`.
Sub-sections use additional `#` levels in a new `chapter()` instance.

**Other methods:**

```python
ch.next()     # advance and return the next number (same as ch())
ch.reset()    # reset counter to zero
ch.open()     # open a new sub-level
ch.close()    # close the current sub-level
```

---

### 5.2 `number` — line numbering

```python
use('number')
n = number(start=1, step=1, fmt="{} ")
```

| Parameter | Default | Meaning |
|-----------|---------|---------|
| `start` | `1` | Starting number |
| `step` | `1` | Increment per line |
| `fmt` | `"{} "` | Python format string; `{}` is replaced with the current number |

**Usage:**

```python
n = number(fmt="{:3d}  ")
doc | n(include("src/main.py"))
```

Each line of the text is prefixed with the formatted counter.

---

### 5.3 `include` — read a file

```python
use('include')
doc | include("path/to/file.txt")
```

Reads the file and returns its full contents as a string.
Errors (file not found, etc.) are propagated and rendered as HTML comments
in the output so the document still generates.

---

### 5.4 `dedent` — strip leading indentation

```python
use('dedent')
doc | dedent(include("src/mymodule.py"))
```

Removes the common leading whitespace from all lines and strips trailing
spaces per line. Useful when including a method or nested block that has
deep indentation in the source file.

---

### 5.5 `snippet` — named code blocks from source files

```python
use('snippet')
src = snippet("src")       # scan the 'src' directory recursively
doc | src("my_function")   # emit the snippet named 'my_function'
```

**How snippets are marked in source files:**

```python
# snippet my_function
def my_function():
    return 42
# end snippet
```

Any comment syntax works (`//`, `#`, `--`, `/* */`, etc.) as long as the
line contains `snippet <name>` or `end snippet`.

```c
// snippet parse_args
int parse_args(int argc, char **argv) { ... }
// end snippet
```

**Key methods:**

```python
src = snippet("src")
src("name")          # return snippet content (or None if not found)
src.get("name")      # same as __call__
src.names()          # list of all snippet names found
src.contains("name") # True/False
src.size()           # number of snippets collected
```

**IMPORTANT for LLMs:** Always use `snippet` to include source code in
documentation. Do **not** copy-paste code into the template. If the code
changes, the documentation will be automatically updated on the next run.

---

### 5.6 `pipe` — composable transformations

```python
use('pipe')
```

`pipe` is an identity transformer. Use `|` to chain transformations:

```python
use('pipe')
use('dedent')
use('number')

n     = number(fmt="{:3d}  ")
clean = pipe | dedent | n      # first dedent, then number lines

doc | clean(include("src/core.py"))
```

Apply a transformation **line by line** with `.on_lines()`:

```python
shout = pipe | str.upper
doc | shout.on_lines()(include("words.txt"))
```

---

### 5.7 `toml` — TOML file reader

```python
use('data/toml')
cfg = toml("pyproject.toml")

doc | cfg.get('project.name')       # -> "pet-doc"
doc | cfg.get('project.version')    # -> "1.0.2"
```

`get("dot.separated.path")` navigates nested tables using `.` as separator.
Numeric segments access list items: `cfg.get("dependencies.0")`.

---

### 5.8 `yaml` — YAML file reader

```python
use('data/yaml')
cfg = yaml("config.yaml")

doc | cfg.get('server.host')
doc | cfg.get('server.port')

for dep in cfg.get('dependencies'):
    doc | dep.get('name') | " " | dep.get('version') | "\n"
```

Same `get()` API as `toml`. Requires `pyyaml` (installed with `pet-doc`).

---

### 5.9 `json` — JSON file reader

```python
use('data/json')
pkg = json("package.json")

doc | pkg.get('name')
doc | pkg.get('version')
doc | pkg.get('scripts.build')
```

Same `get()` API as `toml` and `yaml`.

---

### 5.10 `xml` — XML file reader

```python
use('data/xml')
pom = xml("pom.xml")

doc | pom.xml('version')                          # simple value
doc | pom.xml('properties/java.version')          # nested value
doc | pom.xml("dependencies/dependency[groupId='org.slf4j']/version")

for dep in pom.xml('dependencies'):
    doc | dep.xml('groupId') | ':' | dep.xml('artifactId') | "\n"
```

Namespace prefixes are stripped automatically, so XPath queries work without
the verbose `{uri}tag` syntax. Attribute access:

```python
pom.attr('dependencies/dependency[2]', 'scope')   # -> "test"
```

---

### 5.11 `properties` — Java `.properties` file reader

```python
use('data/properties')
app = properties("application.properties")

doc | app.get('server.host')
doc | app.get('app.version')

for key, value in app:
    doc | key | ' = ' | value | "\n"
```

Keys are looked up **exactly** as written — dots are not path separators
(because dots are valid characters in `.properties` keys).

---

### 5.12 `env` — `.env` file reader

```python
use('data/env')
e = env(".env")

doc | e.get('DATABASE_URL')
doc | e.get('DEBUG')

for key, value in e:
    doc | key | '=' | value | "\n"
```

Strips surrounding quotes (single or double) from values automatically.
Ignores blank lines and lines starting with `#`.

---

## 6. Writing literal `{%` and `%}` in output

PET processes all `{%` ... `%}` blocks. To write the delimiters literally
in the output, build them from parts so PET does not parse them:

```python
{%
OB = '{' + '%'
CB = '%' + '}'
%}

Use {%doc | OB%} and {%doc | CB%} to delimit PET blocks.
```

---

## 7. Common patterns

### Version badge from pyproject.toml

```
{%
use('data/toml')
proj = toml("pyproject.toml")
VERSION = proj.get('project.version')
%}
[![Version](https://img.shields.io/badge/version-{%doc | VERSION%}-orange)](pyproject.toml)
```

### Numbered code listing from a source file

```
{%
use('include')
use('dedent')
use('number')
n = number(fmt="{:3d}  ")
%}

` ` `python
{%doc | n(dedent(include("src/pet/processor.py")))%}
` ` `
```

### Named snippet from source

```
{%
use('snippet')
src = snippet("src")
%}

` ` `python
{%doc | src("my_function")%}
` ` `
```

### Auto-numbered chapter headings

```
{%
use('chapter')
ch = chapter()
%}

{%doc | ch()%} Introduction

{%doc | ch()%} Installation

{%doc | ch()%} Usage
```

Output:
```
# 1 Introduction

# 2 Installation

# 3 Usage
```

---

## 8. LLM instructions for generating PET templates

When writing a `.pet` template:

1. **Never copy-paste source code into a template.** Use `snippet` to pull
   named code blocks directly from source files. This keeps documentation
   in sync when the code changes.

2. **Never hardcode version numbers, dependency names, or configuration values.**
   Read them from `pyproject.toml`, `package.json`, `pom.xml`, or whatever
   config file is the source of truth.

3. **Use `chapter()` for section numbering.** Do not write `# 1`, `# 2`, etc.
   by hand — the numbers will go stale when sections are added or removed.

4. **Use `dedent` when including methods or inner classes** from source files.
   Python methods inside a class have 4–8 spaces of leading indentation that
   should not appear in the documentation.

5. **One setup block at the top.** Load all macros with `use()` in a single
   setup block at the start of the template so readers see all dependencies
   in one place.

6. **`doc |` is the only output mechanism.** Any `print()` calls go to stderr,
   not the output file.

7. **Mark snippets in the source files** with comments the language supports:
   ```
   # snippet function_name      (Python)
   // snippet function_name     (C, Java, JavaScript)
   -- snippet function_name     (SQL, Lua)
   ```
   Then close with `# end snippet` (or `// end snippet`, etc.).

8. **The template IS the documentation intent.** Write templates so that a
   human reading the `.pet` file understands what the output will look like
   without running PET.
