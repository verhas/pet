class env:
    """
    ``.env`` file reader.

    Parses a flat ``KEY=value`` file, ignoring blank lines and lines that
    start with ``#``.  Quoted values (single or double) have their quotes
    stripped.  Keys are looked up directly — no path navigation.

    Example in a template::

        use('data/env')
        e = env(".env")

        doc | e.get('DATABASE_URL')   # -> "postgres://localhost/mydb"
        doc | e.get('DEBUG')          # -> "true"

        for key, value in e:
            doc | key | '=' | value | '\\n'

    :param filename: Path to the ``.env`` file.
    :type filename: str
    """

    def __init__(self, filename):
        self._data = {}
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                    value = value[1:-1]
                self._data[key] = value

    def get(self, key):
        """
        Return the value for ``key``, or ``None`` if the key is absent.

        :param key: The environment variable name.
        :type key: str
        :returns: Value string or ``None``.
        :rtype: str or None
        """
        return self._data.get(key)

    def __iter__(self):
        """Yield ``(key, value)`` pairs for all variables."""
        return iter(self._data.items())

    def __str__(self):
        return ''
