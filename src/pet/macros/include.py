def include(filename):
    """
    Reads a file and returns its contents as a string.

    Errors propagate as exceptions, which the processor renders
    as HTML comments in the output document.

    :param filename: Path to the file to read.
    :type filename: str
    :returns: The full contents of the file.
    :rtype: str
    """
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()
