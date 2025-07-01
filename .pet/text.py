class text:
    """Handles the storage and printing of a text value.

    This class allows storing a string value and provides a callable
    instance to output the stored text. The callable behavior ensures
    the text is printed directly upon invocation.

    Attributes:
        text (str): The string content to be stored and printed.
    """
    def __init__(self, text):
        self.text = text

    def __call__(self, *args, **kwargs):
        print(self.text,end='')