#!/usr/bin/env python3
"""
Template processor that executes Python code blocks between {% %} delimiters.
Usage: python template_processor.py input_file output_file
"""

import sys
import re
import io
from contextlib import redirect_stdout, redirect_stderr
from pathlib import Path


class _Doc:
    """
    Document sink for use in PET templates.

    Provides the ``|`` operator as a concise way to write values into the
    document.  ``doc | value`` prints ``str(value)`` without a trailing
    newline and returns ``doc`` so calls can be chained::

        doc | ch() | " Introduction"
        doc | n(label())
    """

    def __or__(self, value):
        if value is not None:
            print(str(value), end='')
        return self


doc = _Doc()


def process_template(input_file, output_file):
    """
    Process a template file by executing Python code between {% %} delimiters.

    Args:
        input_file (str): Path to input template file
        output_file (str): Path to output file
    """
    try:
        # Read the input file
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # snippet use_function
        def use(what):
            """
            Execute one or more macro files from the ``.pet`` directory.

            ``what`` is a macro name or a glob pattern (without the ``.py``
            extension).  Wildcards follow standard shell conventions::

                use('number')       # load a single macro
                use('*')            # load all macros
                use('inclu*')       # load every macro whose name starts with 'inclu'

            :param what: Macro name or glob pattern (without ``.py`` extension).
            :type what: str
            """
            matches = sorted(Path('.pet').glob(f'{what}.py'))
            if not matches:
                print(f"<!-- ERROR: No macro matching '{what}' found in .pet/ -->")
                return
            for path in matches:
                try:
                    exec(path.read_text(encoding='utf-8'), exec_namespace)
                except Exception as e:
                    print(f"<!-- ERROR executing .pet/{path.name}: {str(e)} -->")
        # end snippet

        def out(*args):
            """Write arguments to the document without a trailing newline."""
            print(*args, sep='', end='')

        # Create a namespace for code execution
        exec_namespace = {
            '__builtins__': __builtins__,
            'use': use,   # Make the use function available to the template code
            'out': out,   # Write to the document without a trailing newline
            'doc': doc,   # Document sink: doc | value writes value to the document
            # Add any global variables you want available to the template code
        }

        # Pattern to match {% ... %} code blocks and {{ ... }} expressions
        pattern = r'\{%\s*(.*?)\s*%\}|\{\{\s*(.*?)\s*\}\}'

        def execute_code_block(match):
            """Execute a {% %} block or evaluate a {{ }} expression."""
            if match.group(1) is not None:
                # {% ... %} — execute as statement(s), capture stdout
                code = match.group(1).strip()
                if not code:
                    return ""
                stdout_capture = io.StringIO()
                stderr_capture = io.StringIO()
                try:
                    with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                        exec(code, exec_namespace, exec_namespace)
                    output = stdout_capture.getvalue()
                    error_output = stderr_capture.getvalue()
                    if error_output:
                        output += f"\n<!-- ERROR: {error_output.strip()} -->"
                    return output
                except Exception as e:
                    return f"<!-- ERROR executing code block: {str(e)} -->"
            else:
                # {{ ... }} — evaluate expression, write result to document
                expr = match.group(2).strip()
                if not expr:
                    return ""
                try:
                    value = eval(expr, exec_namespace, exec_namespace)
                    return "" if value is None else str(value)
                except Exception as e:
                    return f"<!-- ERROR evaluating expression: {str(e)} -->"

        # Replace all {% %} blocks and {{ }} expressions with their output
        processed_content = re.sub(pattern, execute_code_block, content, flags=re.DOTALL)

        # Write the output file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(processed_content)

        print(f"Successfully processed '{input_file}' -> '{output_file}'")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        sys.exit(1)
