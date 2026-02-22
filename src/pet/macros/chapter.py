class chapter:
    """
    A hierarchical counter for numbering chapters in documents with Markdown formatting.
    
    Methods:
    - chapter(): Returns formatted chapter number with an appropriate # prefix
    - open(): Opens a new sublevel starting at 1
    - close(): Closes the current sublevel
    """
    
    def __init__(self, header_prefix="#", sep=" "):
        """Initialize with a single level starting at 0."""
        self.header_prefix = header_prefix
        self.sep = sep
        self.levels = [0]

    def __call__(self):
        """Alias for next()."""
        return self.next()

    def next(self):
        """
        Increment the current level counter and return a formatted chapter string.

        Returns:
            str: Formatted chapter string like "### 1.2.3" where number of # equals level
        """
        # Increment the current (deepest) level
        self.levels[-1] += 1

        # Create the chapter number string (e.g., "1.2.3")
        chapter_number = ".".join(str(level) for level in self.levels)

        prefix = self.header_prefix * len(self.levels)
        return f"{prefix}{self.sep}{chapter_number}"
    
    def open(self):
        """
        Open a new sublevel starting at 0.
        The next next() call will increment it to 1.
        """
        self.levels.append(0)
    
    def close(self):
        """
        Close the current sublevel by removing the deepest level.
        
        Raises:
            ValueError: If trying to close when only one level remains
        """
        if len(self.levels) <= 1:
            raise ValueError("Cannot close the root level")
        
        self.levels.pop()
    
    def reset(self):
        """Reset the counter to initial state."""
        self.levels = [0]
    
    def get_current_level(self):
        """
        Get the current nesting level.
        
        Returns:
            int: Current nesting level (1-based)
        """
        return len(self.levels)
    
    def get_current_numbers(self):
        """
        Get the current chapter numbers as a tuple.
        
        Returns:
            tuple: Current chapter numbers at each level
        """
        return tuple(self.levels)
    
    def __str__(self):
        """String representation showing current state."""
        return f"chapter(levels={self.levels})"
    
    def __repr__(self):
        """Developer representation."""
        return self.__str__()
