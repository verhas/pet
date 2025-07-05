
# 1 Program Enhanced Text (PET) 1.0.0

Program Enhanced Text (PET) is not a program.
It is more of a methodology.
Its aim is to create maintainable documentation using lightweight markup while minimizing manual effort.
After reading this short readme, you’ll see that PET doesn’t introduce anything radically new.
Instead, it leverages existing tools in the simplest possible way to improve documentation quality.

Some may say PET is just text templating—and they wouldn’t be wrong.
Others may describe it as text with macros.
Still others might point to other tools with similar capabilities.

There are many ways to implement PET documentation.
Choose the tool that best suits your purpose and context.

The author of this document has created several tools over the years, which may be used if they best fit your needs.

In this document, we’ll answer key questions about PET:

*  What is PET?

*  What are the issues that PET solves?

*  How to Apply PET in the Most Effective Ways.

## 1.1 What is PET?

PET is a philosophy of document maintenance automation.
Its core principle:

> A human should not maintain any aspect of a document that can be automated.

Consider this simple example: including code samples in documentation.
Traditionally, we copy-paste the code into the document and apply formatting.
When the code changes, we’re supposed to update the document—but often we forget.
Outdated samples remain, causing confusion.

With PET, the document is written in a PET-enhanced format—one step before the final rendered version.
Instead of pasting code, you reference it.
During processing, the referenced code is fetched automatically from the source and included in the document.
When this process is part of your build pipeline, updates are never forgotten.

While the code sample example is common, many other things can be automated:

* Configuration keys that change between versions
* Version numbers
* Lists of features from source code
* And more

If the information already exists somewhere, humans shouldn’t recreate it manually.

Sources can vary.
The sample might come from the documented program, from other parts of the document, or even from the environment.

Regardless of source, if information can be included automatically—it should be.

## 1.2 What are the issues that PET solves?

As mentioned, PET addresses errors caused by redundant, human-maintained information.
Humans are not good at repetitive tasks. Machines are.

Here are the main problems PET solves:

1. **Outdated or inconsistent documentation**
Manually copied content easily falls out of sync with its source. PET eliminates this risk by automating inclusion.

2. **High maintenance costs**
Updating redundant information is time-consuming. PET reduces this burden through automation.

3. **Error-prone duplication**
Redundant, manually maintained data invites inconsistencies. PET enforces a single source of truth.

4. **Delayed updates**
Manual updates are often postponed or skipped. PET integrates updates into the build process, avoiding delays.

5. **Loss of trust in documentation**
Outdated docs erode user confidence. PET helps rebuild trust by ensuring accuracy and timeliness.

##  How to Apply PET in the Most Effective Ways.

To apply PET most effectively, the goal should always be clarity, maintainability, and reduction of manual effort. Here are key strategies:

1. Use a consistent templating engine

Choose a text templating system suitable for your environment.
You can use Jamal, Jinja2, or even a custom processor, like in this document.
Consistency in tooling makes maintenance and onboarding easier.

2. Externalize the changeable

Move all dynamic or frequently changing content (e.g., code samples, config keys, version numbers) out of the static document.
Reference them through PET macros that fetch the current value automatically.

3. Integrate PET processing into the build

Integrate the PET-to-markup transformation into your CI/CD or documentation build pipeline.
This ensures up-to-date documents without requiring manual intervention in separate steps.

4. Use PET selectively

Not all parts of a document benefit from automation. Use PET where redundancy is a risk or where automation yields significant time savings. Avoid adding complexity for its own sake.

5. Validate the output

Automated documentation still needs review. Add validation steps to check that the final rendered documents are complete, readable, and consistent with expectations.

## 1.3 PET the simplest way

This document and the repository are an example of how to use PET with minimal tooling.
The author of this document created Jamal and other similar tools with limited effort.
Jamal, or Pyama, are usable and professional tools, but the starting threshold seems to be too high.
There is a very limited user base for those tools.

It does not mean, however, that PET as a general concept cannot be used.
This repository contains a minimalistic Python script of less than 100 lines that implements the simplest templating ever.
This is enough to use PET.

Include your Python code in the `XYZ.md.pet` document between `{%` and `%}` strings.
Create simple libraries, such as those found in this repository's `.pet` directory.
The templating provides a function `use()` to include these classes and definitions into your document.

To get the `XYZ.md` you can run

```
python3 pet.py XYZ.md.pet XYZ.md
```

or even

```
fswatch -o README.md.pet | xargs -n1 -I{} sh -c 'echo "File changed, regenerating..." && python3 pet.py XYZ.md.pet XYZ.md'
```

to have a constant running background process while you edit your `md.pet` file.

*NOTE:* You can use any format, not only Markdown.

Currently, there are two "macro" classes in this directory.
One can be used to define texts and then use them.
The other one can be used to number sections in Markdown documents.
Later, you may find other simple tools in this repository.

This repository and document illustrate how PET can be applied with minimal tooling.
The author created Jamal and similar tools requiring limited effort.
While these tools are usable and professional, their initial learning curve may seem steep, resulting in a small user base.

However, the concept of PET is not limited to these tools.
This repository contains a minimal Python script—less than 100 lines—that implements a very basic template processor.
This is enough to start using PET.

## 1.4 Summary

