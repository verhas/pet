import yaml as _yaml
from pet.macros.data._node import _DataNode


class yaml(_DataNode):
    """
    YAML file reader with dot-path querying.

    Parses a YAML file and allows querying values using dot-separated paths.
    Nested dicts are returned as ``yaml`` wrappers for further querying.
    Lists are returned as Python lists with dicts wrapped automatically.

    Example in a template::

        use('yaml')
        cfg = yaml("config.yaml")

        doc | cfg.get('server.host')          # -> "localhost"
        doc | cfg.get('server.port')          # -> "8080"

        for dep in cfg.get('dependencies'):
            doc | dep.get('name') | ' ' | dep.get('version') | '\\n'

    Requires PyYAML (``pip install pyyaml``).

    :param filename: Path to the YAML file to parse.
    :type filename: str
    """

    def __init__(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            self._data = _yaml.safe_load(f)
