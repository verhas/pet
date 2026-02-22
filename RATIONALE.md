
# The Rationale Behind PET

> *If information already exists in your project, a human should never maintain
> a second copy of it.*

This document explains why **pet-doc** exists, what problem it
solves, and why that problem is becoming more urgent in the age of
large-language-model tooling.

**Version:** 1.0.0 · **Repo:** https://github.com/verhasp/pet

---

# 1 Documentation Is a Second Copy

Every software project has two representations of its behaviour: the code and
the documentation. The code is the primary source of truth — it is what runs.
The documentation is a copy, written for humans.

This asymmetry is the root of the problem. The code changes continuously under
the pressure of deadlines, bug fixes, and new requirements. The documentation
changes only when someone deliberately decides to update it. In practice, that
rarely happens fast enough.

The result is **documentation drift**: the inevitable, gradual divergence
between what a system does and what its documentation says it does. Drift is
not a failure of discipline — it is a structural consequence of maintaining two
representations of the same facts in two different places by two different
processes.

The correct response is not to ask people to try harder. It is to eliminate the
second copy wherever possible, and to automate its maintenance where elimination
is not possible.

---

# 2 The Single-Source-of-Truth Principle

The DRY principle — *Don't Repeat Yourself* — is well understood in code.
A version number lives in one place; every other reference derives from it.
A configuration schema lives in one file; validation and documentation are
generated from it. Duplication is a liability, not a convenience.

PET applies DRY to documentation. A value that exists in your project —
a version number, an API endpoint, a configuration key, a code sample —
should appear in the documentation **by reference**, not by copy.

In a `.md.pet` template this looks like:

```python
# In the preamble block — one authoritative source:
proj    = toml("pyproject.toml")
VERSION = proj.get('project.version')
```

And in the body:

```
Current release: {% doc | VERSION %}
```

Now `VERSION` appears in the document, but it is not *stored* in the document.
If the release changes, only `pyproject.toml` changes. The documentation
updates automatically on the next `pet.cli:main doc.md.pet doc.md`.

This applies equally to prose. If a section title, product name, or repository
URL appears in multiple places, define it as a variable. At the top of this very
file, `TOOL_NAME`, `VERSION`, and `REPO` are each defined exactly once and
referenced everywhere below. There is no way for them to disagree with each
other or with `pyproject.toml`.

---

# 3 Automating What Can Be Automated

Not every piece of documentation can be derived from code. The *why* behind a
design decision, the conceptual overview that helps a newcomer build a mental
model, the worked example that shows the happy path — these require human
authorship and cannot be automated.

But much of what appears in documentation *can* be automated:

```
 1. Version numbers and release dates
 2. API endpoint paths
 3. Configuration key names and their default values
 4. Data schema field names and types
 5. Code samples that illustrate real, tested behaviour
 6. Section and chapter numbers
 7. Cross-references between documents
 8. Feature lists derived from the codebase
```

Every item in that list is information that already exists in the project.
Asking a human to copy it into documentation is asking them to perform a task
a machine can do perfectly and will never forget to update.

PET's 12 built-in macros cover the most common cases:
data files (`toml`, `yaml`, `json`, `xml`, `properties`, `env`), code inclusion
(`snippet`, `include`), and structural generation (`chapter`, `number`).
Because the macros are plain Python classes, any project-specific automation
— querying a database, calling an internal API, reading a build artefact — can
be added with a single `.py` file dropped into `.pet/`.

---

# 4 Consistency Checks: Document Unit Tests

If a template can read data, it can also *assert* that data satisfies
expectations. This is the document equivalent of a unit test.

Consider a document that claims the public API has a specific response shape.
A consistency check can verify that claim at generation time:

```python
schema = json("api/schema.json")
expected_field = "user_id"
if schema.get(f"properties.{expected_field}") is None:
    sys.exit(
        f"CONSISTENCY FAILURE: field '{expected_field}' not found in api/schema.json.\n"
        f"Either the API changed or the document is wrong. Resolve the discrepancy."
    )
```

If the API is refactored and the field is renamed, the document generation
fails with a clear message. The CI pipeline fails. The stale documentation
never reaches readers.

This document itself contains two such checks, in its opening block:

```
 9. _stated_version = "1.0.0"
10. if VERSION != _stated_version:
11.     sys.exit("version mismatch — update _stated_version or pyproject.toml")
12.
13. _stated_macro_count = 12
14. if MACRO_COUNT != _stated_macro_count:
15.     sys.exit("macro count changed — update _stated_macro_count and the macro list")
```

The first ensures this document stays aligned with the declared release.
The second ensures the macro count mentioned in the text matches the number
of macro files actually present in `src/pet/macros/`. If a macro is added and
this document is not updated, generation fails. The document cannot silently
fall behind the codebase.

**The key insight:** consistency checks turn documentation drift from a silent,
slow failure into a loud, immediate one — the same trade-off that motivates
test-driven development in code.

---

# 5 PET in the Age of Large Language Models

The arguments above have been valid for decades. In the era of LLM tooling,
they become critical.


## 5.1 The RAG Poisoning Problem

Retrieval-Augmented Generation (RAG) systems answer questions by retrieving
relevant documents and providing them as context to an LLM. The LLM then
synthesises an answer from that context.

This architecture has a hidden fragility: **the LLM trusts the retrieved
documents**. That is the explicit design goal of RAG — override the model's
general training with project-specific, current information. When the retrieved
document is accurate, this works brilliantly. When it is stale, it works
brilliantly at producing confident, plausible, wrong answers.

Consider a developer asking a RAG system: *"What arguments does the
`connect()` function accept?"* If the documentation was written for version 1.x
and the codebase is now at 2.x with a changed signature, the LLM will describe
the 1.x signature with complete confidence. It has no way to know the document
is stale — it looks exactly like a current document. The project name is right,
the formatting is familiar, the surrounding context is accurate. Only the
specific fact is wrong.

PET documents sourced from the live codebase cannot have this failure mode for
any fact that is derived rather than written. A function signature included via
`snippet`, a configuration key read via `toml`, an endpoint path read from a
schema — these are accurate at generation time, by construction. The only
question is how recently the document was last generated, and that is a CI/CD
question, not a documentation-quality question.

## 5.2 The LLM-Assisted Writing Problem

The second dimension is the use of LLMs to *write* documentation. This
introduces a subtler risk: **implicit copying**.

When an LLM helps draft a section of documentation, it draws on the context
it has been given — existing docs, code snippets, its conversation history.
If it sees the string `"v1.3.2"` in that context, it may write `"v1.3.2"` into
the new section. This is not a reference; it is a copy. It will drift the
moment the version changes.

More insidiously: an LLM tasked with updating one section of a document will
not automatically update other sections that refer to the same facts. It
updates what it is asked about. The result is a document that is internally
inconsistent — some sections updated, others not — with no obvious signal to
the reader that anything is wrong.

PET changes the contract between the author and the LLM:

- The LLM authors **prose** — narrative, explanation, motivation. This is where
  LLMs genuinely excel and where automation is inappropriate.
- PET provides **facts** — values read from authoritative sources at generation
  time. The LLM never touches these.

In practice this means the LLM edits `.md.pet` files, not `.md` files. It
writes `{% doc | VERSION %}` in the source, not `"1.0.0"`.
The separation is enforced structurally: the variable is defined once, and the
LLM has no mechanism to introduce a second copy.

There is a further advantage that is easy to overlook: **PET templates are
written in plain Python, and LLMs handle Python exceptionally well.** Every
LLM of any consequence has been trained on vast amounts of Python code. The
templating constructs — reading a TOML file, asserting a condition, formatting
a string — are idiomatic Python that any capable LLM writes fluently and
correctly. Contrast this with proprietary templating DSLs: Jinja2 edge cases,
Velocity syntax, Handlebars subtleties, the idiosyncratic rules of a bespoke
system. Each of those requires the LLM to have seen enough examples of that
specific system to reason about it reliably. Python requires no such
specialisation. An LLM asked to write a consistency check, add a new macro
call, or restructure a PET preamble will do so correctly on the first attempt,
because it is just writing Python.

This document is a concrete demonstration of that claim. The entire
`RATIONALE.md.pet` — section structure, live variable definitions, data
sourced from `pyproject.toml`, numbered lists generated at build time, and
all consistency checks that will fail the build if the code diverges from the
prose — was produced in response to a single prompt. No iteration was needed
on the template logic. The Python was correct immediately, because it is Python.

## 5.3 The Compounding Problem

The two risks above combine into a feedback loop.

A developer uses an LLM to write documentation for a new feature. The LLM
draws context from existing documentation, some of which is already slightly
stale. It reproduces the stale values — version numbers, field names, endpoint
paths — into the new documentation, because they were present in its context
and it had no reason to question them.

The new documentation is published. A RAG system indexes it. The next developer
who queries the RAG system receives answers that are now stale *plus one more
generation of drift*. They use an LLM to write documentation based on those
answers. The cycle repeats with compounding errors.

This is not a theoretical risk. It is the documentation equivalent of a genetic
copy error — small per generation, but cumulative and directional. Without a
forcing function that catches drift, the documentation knowledge base degrades
monotonically.

PET is that forcing function. Every derived value in a PET template is
re-evaluated at generation time from its authoritative source. Consistency
checks fail the build when prose claims diverge from code reality. The template
structure makes it explicit — to both human authors and LLM assistants — which
values are authoritative and where they come from.



---

# 6 In Practice

The shift PET asks for is a small change in habit with a large change in
outcome:

**Instead of** writing `"version 1.0.0"` in a document, write
`{% doc | VERSION %}` and define `VERSION` once from
`pyproject.toml`.

**Instead of** pasting a code sample, write
`{% doc | n(src('example')) %}` and let `snippet` pull
the live sample from the tested source.

**Instead of** hoping someone notices when a field name changes, write a
consistency check that makes the document fail to generate if the field
disappears.

**Instead of** giving an LLM a static `.md` file to update, give it the
`.md.pet` template and let it work at the level of intent, not values.

None of this prevents documentation from requiring human thought and care.
It prevents documentation from requiring human *copying* — the part that
machines do better, and that humans inevitably do worse as time pressure grows.

---

*Generated from `RATIONALE.md.pet` by pet-doc 1.0.0 ·
`pet.cli:main RATIONALE.md.pet RATIONALE.md`*
