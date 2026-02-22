import tomllib
from pet.macros.data._node import _DataNode


class toml(_DataNode):
    """
    TOML file reader with dot-path querying.

    Parses a TOML file and allows querying values using dot-separated paths.
    Nested tables are returned as ``toml`` wrappers for further querying.
    Arrays are returned as Python lists with tables wrapped automatically.

    Example in a template::

        use('toml')
        cfg = toml("pyproject.toml")

        doc | cfg.get('project.name')       # -> "pet-doc"
        doc | cfg.get('project.version')    # -> "1.0.0"

        for dep in cfg.get('dependencies'):
            doc | dep.get('name') | '\\n'

    Requires Python 3.11+ (uses the standard library ``tomllib`` module).

    :param filename: Path to the TOML file to parse.
    :type filename: str
    """

    def __init__(self, filename):
        with open(filename, 'rb') as f:
            self._data = tomllib.load(f)
