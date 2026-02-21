import textwrap


def dedent(text):
    """
    Remove common leading whitespace and trailing whitespace from each line.

    Strips trailing spaces from every line, then removes the common leading
    indentation so the leftmost non-empty line starts at column zero while
    preserving the relative indentation of all other lines.

    Useful for including code snippets that are deeply indented in the source
    file (e.g. a method inside a class) without carrying all that indentation
    into the documentation.

    Example::

        dedent('''
                def foo():
                    return 42
                ''')
        # -> "def foo():\\n    return 42"

    :param text: A block of text, typically a code snippet.
    :type text: str
    :returns: The text with common indentation and trailing spaces removed.
    :rtype: str
    """
    lines = [line.rstrip() for line in text.split('\n')]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return textwrap.dedent('\n'.join(lines))
