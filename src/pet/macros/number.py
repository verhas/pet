class number:
    """
    Line numbering tool for code blocks in documentation.

    Takes a block of text, splits it into individual lines, and prepends
    a sequential number to each line. Designed for numbering code samples
    included in documents via the ``snippet`` or ``include`` macros.

    The counter persists across calls, so multiple blocks can be numbered
    continuously. To restart numbering, simply create a new instance.

    Uses standard Python format strings for number formatting.
    A negative ``step`` produces decreasing line numbers.

    Formatting examples::

        number()                   # "1", "2", "3"        (default, plain number)
        number(fmt="{:03d}")       # "001", "002", "003"  (zero-padded, width 3)
        number(fmt="{:4d}")        # "   1", "   2"       (right-aligned, width 4)
        number(fmt="{:x}")         # "1", "2", ... "a"    (hexadecimal)
        number(start=10, step=-1)  # "10", "9", "8"       (decreasing)

    Example in a template::

        use('snippet')
        use('number')
        snippets = Snippet("src")
        n = number(fmt="{:3d} ")
        doc | n(snippets('main'))   # -> numbered lines of the snippet
    """

    def __init__(self, start=1, step=1, fmt="{} "):
        """
        Initialize the line numbering tool.

        :param start: Starting value of the counter (default: 1).
        :type start: int
        :param step: Increment between consecutive line numbers (default: 1).
            Use a negative value for decreasing numbers.
        :type step: int
        :param fmt: Python format string for the number (default: ``"{} "``,
            plain number and a space). Use the standard Python format specification
            mini-language. Examples: ``"{:03d}"`` for zero-padded width 3,
            ``"{:4d}"`` for right-aligned width 4, ``"{:x}"`` for hexadecimal.
        :type fmt: str
        """
        self.count = start
        self.step = step
        self.fmt = fmt

    def __call__(self, text):
        """
        Number each line of the given text block and return the result.

        Splits ``text`` on newlines, prepends the current counter-value to
        each line, then it returns all numbered lines joined by ``\\n``.
        Leading and trailing whitespace is stripped before splitting, so
        triple-quoted strings and files ending with ``\\n`` work naturally.
        Empty lines receive the number only, without a trailing space.

        :param text: A block of text (typically a code snippet) to be numbered.
        :type text: str
        :returns: The text with each line prefixed by a sequential number.
        :rtype: str
        """
        lines = text.strip().split('\n')
        result = []
        for line in lines:
            num = self.fmt.format(self.count)
            self.count += self.step
            result.append(f"{num}{line}" if line else num.rstrip())
        return '\n'.join(result)
