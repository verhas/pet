import xml.etree.ElementTree as ET


class xml:
    """
    XML file reader with XPath querying.

    Parses an XML file and allows querying values by XPath expression.
    Namespace prefixes are stripped automatically, so queries work without
    knowing the namespace URI — useful for files like Maven POM where the
    default namespace would otherwise require verbose ``{uri}tag`` syntax.

    Return value of ``xml(xpath)`` depends on what the path matches:

    * **Nothing** → ``None``
    * **One leaf element** (no children) → text string
    * **One complex element** (has children) → ``xml`` wrapper, iterable
      and queryable with further ``xml()`` calls
    * **Multiple elements** → list of text strings or ``xml`` wrappers,
      following the same leaf/complex rule per element

    Example in a template::

        use('xml')
        pom = xml("pom.xml")

        # simple value
        doc | pom.xml('version')                          # -> "1.2.3"

        # nested value
        doc | pom.xml('properties/java.version')          # -> "17"

        # predicate: version of a specific dependency
        doc | pom.xml("dependencies/dependency[groupId='org.slf4j']/version")

        # multiple leaf values
        for aid in pom.xml('dependencies/dependency/artifactId'):
            doc | aid | '\\n'

        # iterate over complex elements
        for dep in pom.xml('dependencies'):
            doc | dep.xml('groupId') | ':' | dep.xml('artifactId') | '\\n'

    :param filename: Path to the XML file to parse.
    :type filename: str
    """

    def __init__(self, filename):
        root = ET.parse(filename).getroot()
        for elem in root.iter():
            if '}' in elem.tag:
                elem.tag = elem.tag.split('}', 1)[1]
        self._root = root

    @classmethod
    def _from_element(cls, element):
        obj = object.__new__(cls)
        obj._root = element
        return obj

    def _wrap(self, element):
        """Return text for leaf elements, an xml wrapper for complex ones."""
        if len(element) == 0:
            return element.text
        return xml._from_element(element)

    def xml(self, xpath):
        """
        Query the XML by XPath and return the result.

        :param xpath: XPath expression relative to the current element.
        :type xpath: str
        :returns: ``None``, a string, an ``xml`` wrapper, or a list thereof.
        """
        matches = self._root.findall(xpath)
        if not matches:
            return None
        results = [self._wrap(e) for e in matches]
        return results[0] if len(results) == 1 else results

    def attr(self, xpath, attribute):
        """
        Return the value of an XML attribute on the element(s) matched by ``xpath``.

        Follows the same single/multiple return convention as ``xml()``:
        a single match returns a string (or ``None`` if the attribute is absent),
        multiple matches return a list.

        Example::

            pom.attr('dependencies/dependency[2]', 'scope')   # -> "test"
            pom.attr('dependencies/dependency', 'scope')
            # -> [None, 'test', 'compile']

        :param xpath: XPath expression relative to the current element.
        :type xpath: str
        :param attribute: Name of the XML attribute to read.
        :type attribute: str
        :returns: Attribute value string, ``None``, or a list thereof.
        """
        matches = self._root.findall(xpath)
        if not matches:
            return None
        results = [e.get(attribute) for e in matches]
        return results[0] if len(results) == 1 else results

    def __iter__(self):
        """Iterate over direct child elements."""
        for child in self._root:
            yield self._wrap(child)

    def __str__(self):
        return (self._root.text or '').strip()
