#!/usr/bin/env python3
"""
Template processor that executes Python code blocks between {% %} delimiters.
Usage: python template_processor.py input_file output_file
"""

import sys
import re
import io
from contextlib import redirect_stdout, redirect_stderr


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

        def use(what):
            """
            Executes a Python script stored inside a specific `.pet` directory.

            This function dynamically reads and executes a Python file based on the provided
            filename. The file is located in the `.pet` directory relative to the current
            working directory. Use this function with caution, as dynamically executing
            code can pose a security risk if the source is not trusted.

            :param what: Name of the script (without the `.py` extension) located within
                the `.pet` folder.
            :type what: str
            """
            try:
                with open(f".pet/{what}.py", 'r', encoding='utf-8') as f:
                    code = f.read()
                exec(code, exec_namespace)
            except FileNotFoundError:
                print(f"<!-- ERROR: File '.pet/{what}.py' not found -->")
            except Exception as e:
                print(f"<!-- ERROR executing .pet/{what}.py: {str(e)} -->")

        # Create a namespace for code execution
        exec_namespace = {
            '__builtins__': __builtins__,
            'use': use,  # Make the use function available to the template code
            # Add any global variables you want available to the template code
        }

        # Pattern to match {% ... %} blocks
        pattern = r'\{%\s*(.*?)\s*%\}'

        def execute_code_block(match):
            """Execute a single code block and return its output."""
            code = match.group(1).strip()

            if not code:
                return ""

            # Capture stdout and stderr
            stdout_capture = io.StringIO()
            stderr_capture = io.StringIO()

            try:
                # Redirect stdout and stderr to capture output
                with redirect_stdout(stdout_capture), redirect_stderr(stderr_capture):
                    # Execute the code and update the namespace with any new variables
                    exec(code, exec_namespace, exec_namespace)

                # Get the captured output
                output = stdout_capture.getvalue()
                error_output = stderr_capture.getvalue()

                # If there were errors, include them in the output
                if error_output:
                    output += f"\n<!-- ERROR: {error_output.strip()} -->"

                return output

            except Exception as e:
                # Return error information as a comment
                return f"<!-- ERROR executing code block: {str(e)} -->"

        # Replace all {% %} blocks with their executed output
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


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) != 3:
        print("Usage: python template_processor.py <input_file> <output_file>")
        print("\nExample:")
        print("  python template_processor.py template.txt output.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    process_template(input_file, output_file)


if __name__ == "__main__":
    main()
