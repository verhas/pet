class properties:
    """
    Java ``.properties`` file reader.

    Parses a flat ``key=value`` (or ``key: value``) file, ignoring lines
    that start with ``#`` or ``!``.  Keys are looked up directly — dot
    notation is **not** split into path segments, because dots are valid
    characters in ``.properties`` keys (e.g. ``server.host``).

    Example in a template::

        use('data/properties')
        app = properties("application.properties")

        doc | app.get('server.host')     # -> "localhost"
        doc | app.get('app.version')     # -> "1.0.0"

        for key, value in app:
            doc | key | ' = ' | value | '\\n'

    :param filename: Path to the ``.properties`` file.
    :type filename: str
    """

    def __init__(self, filename):
        self._data = {}
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#') or line.startswith('!'):
                    continue
                for sep in ('=', ':'):
                    if sep in line:
                        key, value = line.split(sep, 1)
                        self._data[key.strip()] = value.strip()
                        break

    def get(self, key):
        """
        Return the value for ``key``, or ``None`` if the key is absent.

        :param key: The exact property key, including any dots.
        :type key: str
        :returns: Value string or ``None``.
        :rtype: str or None
        """
        return self._data.get(key)

    def __iter__(self):
        """Yield ``(key, value)`` pairs for all properties."""
        return iter(self._data.items())

    def __str__(self):
        return ''
