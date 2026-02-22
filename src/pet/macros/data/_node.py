class _DataNode:
    """
    Shared base for YAML, JSON, and TOML data wrappers.

    Provides dot-separated path navigation, list-index access, iteration,
    and automatic wrapping of nested dicts in the same subclass.
    """

    @classmethod
    def _from_data(cls, data):
        obj = object.__new__(cls)
        obj._data = data
        return obj

    def _wrap(self, value):
        if isinstance(value, dict):
            return self.__class__._from_data(value)
        if isinstance(value, list):
            return [self._wrap(v) for v in value]
        return value

    def get(self, path):
        """
        Navigate the data using a dot-separated key path.

        Each segment of ``path`` is used as a dict key; numeric segments
        are used as list indices.  Returns ``None`` if any step is missing.

        .. note::
            Keys that contain a literal dot cannot be reached with this
            method — navigate step by step via intermediate ``get()`` calls.

        :param path: Dot-separated key path, e.g. ``'server.host'`` or
            ``'dependencies.0.name'``.
        :type path: str
        :returns: Scalar value, a wrapped node for dicts, a list for arrays,
            or ``None`` if the path does not exist.
        """
        current = self._data
        for key in path.split('.'):
            if current is None:
                return None
            if isinstance(current, list):
                try:
                    current = current[int(key)]
                except (ValueError, IndexError):
                    return None
            elif isinstance(current, dict):
                current = current.get(key)
            else:
                return None
        return self._wrap(current)

    def __iter__(self):
        """Iterate over list items or dict values, wrapping dicts."""
        items = self._data if isinstance(self._data, list) else (
            self._data.values() if isinstance(self._data, dict) else []
        )
        for item in items:
            yield self._wrap(item)

    def __str__(self):
        if isinstance(self._data, (dict, list)) or self._data is None:
            return ''
        return str(self._data)
