# include() Function Documentation

## Overview

The `include()` function reads the contents of a text file and prints all lines to the console. It provides basic error handling for common file operations issues.

## Syntax

```python
include(filename)
```

## Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `filename` | `str` | The path to the file to be read and printed |

## Return Value

This function does not return a value (`None`). It prints output directly to the console.

## Behavior

1. Opens the specified file in read mode with UTF-8 encoding
2. Reads all lines from the file into memory
3. Prints the entire file content to the console as a single string
4. Handles errors gracefully with informative error messages

## Error Handling

The function includes comprehensive error handling for common file operation issues:

- **FileNotFoundError**: Displays a user-friendly message when the specified file doesn't exist
- **General Exception**: Catches and displays any other errors that may occur during file reading (e.g., permission errors, encoding issues)

## Examples

### Basic Usage

```python
# Print contents of a text file
include("config.txt")

# Print contents of a Python file
include("script.py")

# Use with relative path
include("data/sample.txt")

# Use with absolute path
include("/home/user/documents/readme.md")
```

### Error Scenarios

```python
# File doesn't exist
include("nonexistent.txt")
# Output: Error: File 'nonexistent.txt' not found

# Permission denied or other errors
include("/root/protected_file.txt")
# Output: Error reading file '/root/protected_file.txt': [Permission denied]
```

## Notes

- The function reads the entire file into memory, which may not be suitable for very large files
- Files are opened with UTF-8 encoding by default
- The output preserves the original file formatting including line breaks and whitespace
- No modification or processing of the file content occurs - it's printed exactly as stored

## Use Cases

- Displaying configuration files
- Showing file contents for debugging
- Including template files in output
- Quick file content inspection
- Educational demonstrations of file reading