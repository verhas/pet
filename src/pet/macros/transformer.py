class Transformer:
    """
    A class that wraps a transformation function and makes it callable.
    Allows you to create reusable text transformations using lambdas.
    """
    
    def __init__(self, transform_func):
        """
        Initialize the transformer with a transformation function.
        
        Args:
            transform_func: A function that takes a string and returns a string
        """
        self.transform_func = transform_func
    
    def __call__(self, text):
        """
        Apply the transformation to the given text.
        
        Args:
            text: The string to transform
            
        Returns:
            The transformed string
        """
        return self.transform_func(text)
    
    def compose(self, other_transformer):
        """
        Compose this transformer with another transformer.
        
        Args:
            other_transformer: Another Transformer instance
            
        Returns:
            A new Transformer that applies both transformations
        """
        return Transformer(lambda text: other_transformer(self(text)))

# Example usage demonstrations
if __name__ == "__main__":
    # Example utility functions for text transformation
    def strip_leading_spaces(text):
        """Remove leading spaces from each line."""
        return '\n'.join(line.lstrip(' ') for line in text.split('\n'))


    def number_lines(text, start=1):
        """Add line numbers to each line."""
        lines = text.split('\n')
        return '\n'.join(f"{i + start}: {line}" for i, line in enumerate(lines))


    def add_prefix(text, prefix):
        """Add a prefix to each line."""
        return '\n'.join(f"{prefix}{line}" for line in text.split('\n'))


    def uppercase_text(text):
        """Convert text to uppercase."""
        return text.upper()


    # Sample text with leading spaces
    sample_text = """    Hello World
    This is a test
        With various indentation
    End of text"""
    
    print("Original text:")
    print(repr(sample_text))
    print("\n" + "="*50 + "\n")
    
    # Example 1: Simple transformation using lambda
    strip_spaces = Transformer(lambda text: strip_leading_spaces(text))
    
    print("After stripping leading spaces:")
    result1 = strip_spaces(sample_text)
    print(repr(result1))
    print("\n" + "="*50 + "\n")
    
    # Example 2: Using partial application for parameterized functions
    from functools import partial
    
    # Create a transformer that numbers lines starting from 1
    line_numberer = Transformer(lambda text: number_lines(text, start=1))
    
    print("After numbering lines:")
    result2 = line_numberer(result1)
    print(repr(result2))
    print("\n" + "="*50 + "\n")
    
    # Example 3: Composing multiple transformations
    # First strip spaces, then number lines
    combined_transformer = strip_spaces.compose(line_numberer)
    
    print("Combined transformation (strip + number):")
    result3 = combined_transformer(sample_text)
    print(repr(result3))
    print("\n" + "="*50 + "\n")
    
    # Example 4: More complex lambda with currying-like behavior
    def create_prefixer(prefix):
        """Factory function that returns a prefixing transformer."""
        return Transformer(lambda text: add_prefix(text, prefix))
    
    bullet_point_transformer = create_prefixer("• ")
    
    print("Adding bullet points:")
    result4 = bullet_point_transformer(result1)
    print(repr(result4))
    print("\n" + "="*50 + "\n")
    
    # Example 5: Chaining multiple transformations
    complex_transformer = (Transformer(lambda text: strip_leading_spaces(text))
                          .compose(Transformer(lambda text: number_lines(text, start=1)))
                          .compose(Transformer(lambda text: add_prefix(text, ">>> "))))
    
    print("Complex chained transformation:")
    result5 = complex_transformer(sample_text)
    print(repr(result5))
    print("\n" + "="*50 + "\n")
    
    # Example 6: Using closure to create parameterized transformers
    def create_numbered_transformer(start_num=1, prefix=""):
        """Create a transformer that numbers lines with optional prefix."""
        return Transformer(
            lambda text: '\n'.join(
                f"{prefix}{i + start_num}: {line}" 
                for i, line in enumerate(text.split('\n'))
            )
        )
    
    custom_numberer = create_numbered_transformer(start_num=10, prefix="Line ")
    
    print("Custom numbered transformation:")
    result6 = custom_numberer(result1)
    print(repr(result6))