import json as _json
from pet.macros.data._node import _DataNode


class json(_DataNode):
    """
    JSON file reader with dot-path querying.

    Parses a JSON file and allows querying values using dot-separated paths.
    Nested objects are returned as ``json`` wrappers for further querying.
    Arrays are returned as Python lists with objects wrapped automatically.

    Example in a template::

        use('json')
        pkg = json("package.json")

        doc | pkg.get('name')               # -> "my-app"
        doc | pkg.get('version')            # -> "1.0.0"
        doc | pkg.get('scripts.build')      # -> "webpack"

        for dep in pkg.get('dependencies'):
            doc | dep.get('name') | '\\n'

    :param filename: Path to the JSON file to parse.
    :type filename: str
    """

    def __init__(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            self._data = _json.load(f)
