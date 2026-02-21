class Pipe:
    """
    A composable text transformation pipeline.

    Start with the module-level ``pipe`` identity instance and chain
    transformations using ``|`` or ``and_then``::

        pipe | dedent | number(fmt="{:3d} ")

    Each ``|`` stage accepts any callable (plain function or another ``Pipe``).
    """

    def __init__(self):
        self._func = lambda x: x

    @classmethod
    def _make(cls, func):
        p = cls()
        p._func = func
        return p

    def __call__(self, text):
        return self._func(text)

    def and_then(self, other_func):
        """
        Compose this pipe with a callable applied after self.

        ``a.and_then(b)`` is equivalent to ``a | b``.

        Args:
            other_func: A callable that takes a string and returns a string

        Returns:
            A new Pipe that applies self first, then other_func
        """
        return Pipe._make(lambda text: other_func(self(text)))

    def __or__(self, other_func):
        """
        Pipe operator: compose this pipe with the next callable.

        Allows chaining with ``|`` syntax::

            pipe | dedent | number(fmt="{:3d} ")

        Equivalent to ``and_then``.

        Args:
            other_func: A callable that takes a string and returns a string

        Returns:
            A new Pipe that applies self first, then other_func
        """
        return self.and_then(other_func)

    def on_lines(self):
        """
        Return a new Pipe that applies this transformation to each line
        individually, leaving the line structure intact.

        Useful when the wrapped function is designed for a single line, but you
        want to apply it across a multi-line block::

            (pipe | str.strip).on_lines()("  hello  \\n  world  ")
            # -> "hello\\nworld"

        Returns:
            A new Pipe that maps self over each line
        """
        return Pipe._make(lambda text: '\n'.join(self(line) for line in text.split('\n')))


pipe = Pipe()
