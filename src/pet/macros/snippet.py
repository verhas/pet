import os
import re
from typing import Dict, Optional


class Snippet:
    """
    A class to recursively scan files in a directory and collect code snippets.

    Snippets are defined by:
    - Start: a line containing "snippet <name>" where <name> is an identifier
    - End: a line containing "end snippet" (with optional spaces between words)
    """

    def __init__(self, directory: str):
        """
        Initialize the Snippet and scan the directory for snippets.

        Args:
            directory (str): The directory path to scan recursively
        """
        self.directory = directory
        self.snippets: Dict[str, str] = {}
        self._scan_directory()

    def _scan_directory(self):
        """Recursively scan the directory and collect all snippets."""
        if not os.path.exists(self.directory):
            raise ValueError(f"Directory '{self.directory}' does not exist")

        if not os.path.isdir(self.directory):
            raise ValueError(f"'{self.directory}' is not a directory")

        for root, dirs, files in os.walk(self.directory):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    self._extract_snippets_from_file(file_path)
                except (UnicodeDecodeError, PermissionError):
                    # Skip files that can't be read as text or don't have permission
                    continue

    def _extract_snippets_from_file(self, file_path: str):
        """
        Extract snippets from a single file.

        Args:
            file_path (str): Path to the file to process
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Check for snippet start pattern
            snippet_match = self._match_snippet_start(line)
            if snippet_match:
                snippet_name = snippet_match
                snippet_content = []
                i += 1  # Move to next line after snippet declaration

                # Collect lines until we find the end snippet marker
                while i < len(lines):
                    line = lines[i]

                    if self._match_snippet_end(line.strip()):
                        if self.snippets.get(snippet_name):
                            raise ValueError(f"Snippet '{snippet_name}' already exists in the file '{file_path}'")
                        # Found end marker, store the snippet
                        self.snippets[snippet_name] = ''.join(snippet_content)
                        break
                    else:
                        snippet_content.append(line)

                    i += 1

                # If we reached EOF without finding 'end' marker
                if i >= len(lines) and snippet_content:
                    raise ValueError(f"Snippet '{snippet_name}' is not terminated in the file '{file_path}'")

            i += 1

    def _match_snippet_start(self, line: str) -> Optional[str]:
        """
        Check if a line matches the snippet start pattern and extract the name.

        Args:
            line (str): The line to check

        Returns:
            Optional[str]: The snippet name if found, None otherwise
        """
        # Pattern: any characters, "snippet", whitespace, identifier, any characters
        # The identifier should be a valid Python identifier (letters, digits, underscore)
        pattern = r'.*snippet\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        match = re.search(pattern, line, re.IGNORECASE)

        if match:
            return match.group(1)
        return None

    def _match_snippet_end(self, line: str) -> bool:
        """
        Check if a line matches the snippet end pattern.

        Args:
            line (str): The line to check

        Returns:
            bool: True if the line matches the end pattern
        """
        # Pattern: any characters, "end", whitespace, "snippet", any characters
        pattern = r'.*end\s+snippet.*'
        return bool(re.search(pattern, line, re.IGNORECASE))

    def get(self, name: str) -> Optional[str]:
        """
        Get a snippet by its name.

        Args:
            name (str): The name of the snippet to retrieve

        Returns:
            Optional[str]: The snippet content if found, None otherwise
        """
        return self.snippets.get(name)

    def __call__(self, name: str):
        """
        Return a snippet by its name.

        Args:
            name (str): The name of the snippet to retrieve

        Returns:
            Optional[str]: The snippet content if found, None otherwise
        """
        return self.get(name)

    def names(self) -> list:
        """
        Get a list of all available snippet names.

        Returns:
            list: List of snippet names
        """
        return list(self.snippets.keys())

    def contains(self, name: str) -> bool:
        """
        Check if a snippet with the given name exists.

        Args:
            name (str): The name of the snippet to check

        Returns:
            bool: True if the snippet exists, False otherwise
        """
        return name in self.snippets

    def size(self) -> int:
        """
        Get the total number of snippets collected.

        Returns:
            int: Number of snippets
        """
        return len(self.snippets)

    def __str__(self) -> str:
        """String representation of the Snippet."""
        return f"Snippet(directory='{self.directory}', snippets={len(self.snippets)})"

    def __repr__(self) -> str:
        """Detailed string representation of the Snippet."""
        return f"Snippet(directory='{self.directory}', snippets={list(self.snippets.keys())})"


# Example usage
if __name__ == "__main__":
    # Example of how to use the Snippet

    # Create a collector for the current directory
    collector = Snippet(".")

    print(f"Found {collector.size()} snippets")
    print(f"Snippet names: {collector.names()}")

    # Get a specific snippet
    if collector.contains("MySnippet"):
        content = collector.get("MySnippet")
        print(f"MySnippet content:\n{content}")
    else:
        print("MySnippet not found")
