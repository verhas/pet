class ChapterCounter:
    """
    A hierarchical counter for numbering chapters in documents with Markdown formatting.
    
    Methods:
    - chapter(): Returns formatted chapter number with appropriate # prefix
    - open(): Opens a new sublevel starting at 1
    - close(): Closes the current sublevel
    """
    
    def __init__(self):
        """Initialize with a single level starting at 0."""
        self.levels = [0]  # Start with one level at 0

    def __call__(self):
        """Alias for chapter()."""
        return self.chapter()

    def chapter(self):
        """
        Increment the current level counter and return a formatted chapter string.
        
        Returns:
            str: Formatted chapter string like "### 1.2.3" where number of # equals level
        """
        # Increment the current (deepest) level
        self.levels[-1] += 1
        
        # Create the chapter number string (e.g., "1.2.3")
        chapter_number = ".".join(str(level) for level in self.levels)
        
        # Create the markdown header with appropriate number of # characters
        level = len(self.levels)
        header_prefix = "#" * level
        
        print( f"{header_prefix} {chapter_number}", end = '')
    
    def open(self):
        """
        Open a new sublevel starting at 0.
        The next chapter() call will increment it to 1.
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
        return f"ChapterCounter(levels={self.levels})"
    
    def __repr__(self):
        """Developer representation."""
        return self.__str__()


# Example usage and demonstration
if __name__ == "__main__":
    print("=== Chapter Counter Demo ===\n")
    
    counter = ChapterCounter()
    
    # Main chapters
    print(counter.chapter())  # # 1
    print("Introduction content here...\n")
    
    print(counter.chapter())  # # 2
    print("Background content here...")
    
    # Open sublevel for sections
    counter.open()
    print(counter.chapter())  # ## 2.1
    print("First section content...")
    
    print(counter.chapter())  # ## 2.2
    print("Second section content...")
    
    # Open another sublevel for subsections
    counter.open()
    print(counter.chapter())  # ### 2.2.1
    print("First subsection content...")
    
    print(counter.chapter())  # ### 2.2.2
    print("Second subsection content...")
    
    # Close subsection level
    counter.close()
    print(counter.chapter())  # ## 2.3
    print("Third section content...")
    
    # Close section level
    counter.close()
    print(counter.chapter())  # # 3
    print("Next main chapter content...")
    
    print(f"\nCurrent state: {counter}")
    print(f"Current level: {counter.get_current_level()}")
    print(f"Current numbers: {counter.get_current_numbers()}")
