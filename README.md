
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

To apply PET effectively, aim for clarity, maintainability, and reduced manual work.
Here are the key strategies:

1. **Use a consistent templating engine**
Choose one appropriate for your environment—Jamal, Jinja2, or even a simple custom engine like in this document.
Consistency improves maintainability and onboarding.

2. **Externalize the changeable**
Move frequently changing elements (code, config keys, version numbers) out of the document body.
Reference them with PET macros that fetch the current value.

3. **Integrate PET into the build process**
Add PET rendering to your CI/CD or documentation build pipeline.
This ensures documents stay up to date automatically.

4. **Use PET selectively**
Not all content benefits from automation. Use PET where it reduces redundancy and saves time.
Avoid unnecessary complexity.

5. **Validate the output**
Even automated documentation requires review.
Add validation steps to ensure rendered output is complete, correct, and clear.

## 1.3 PET the Simplest Way

This repository and document illustrate how PET can be applied with minimal tooling.
The author created Jamal and similar tools requiring limited effort.
While these tools are usable and professional, their initial learning curve may seem steep, resulting in a small user base.

However, the concept of PET is not limited to these tools.
This repository contains a minimal Python script—less than 100 lines—that implements a very basic template processor.
This is enough to start using PET.

Include Python code in your `XYZ.md.pet` file between `<!-- ERROR executing code block: invalid syntax (<string>, line 1) -->` markers.
Create small reusable libraries, as seen in the `.pet` directory.
The `use()` function includes these resources into your PET document.

To generate your output file `XYZ.md`, use: