# Snippet Class Documentation

The `Snippet` class is a utility for recursively scanning directories to collect and manage code snippets from files. It automatically extracts snippets based on specific comment markers and provides convenient methods to access them.

## Overview

Snippets are defined by:
- **Start marker**: A line containing `snippet <name>` where `<name>` is a valid identifier
- **End marker**: A line containing `end snippet` (with optional spaces between words)

The class supports various comment styles (e.g., `//`, `#`, `/* */`) and is case-insensitive for the snippet keywords.

## Constructor

### `Snippet(directory: str)`

Creates a new Snippet instance and automatically scans the specified directory for snippets.

**Parameters:**
- `directory` (str): The directory path to scan recursively for snippet files

**Raises:**
- `ValueError`: If the directory doesn't exist or is not a valid directory
- `ValueError`: If duplicate snippet names are found
- `ValueError`: If snippets are not properly terminated with end markers

**Example:**
```python
collector = Snippet("/path/to/code")
```

## Public Methods

### `get(name: str) -> Optional[str]`

Retrieves the content of a specific snippet by name.

**Parameters:**
- `name` (str): The name of the snippet to retrieve

**Returns:**
- `Optional[str]`: The snippet content as a string if found, `None` otherwise

**Example:**
```python
content = collector.get("MyFunction")
if content:
    print(content)
```

### `names() -> list`

Returns a list of all available snippet names.

**Returns:**
- `list`: List of snippet names (strings)

**Example:**
```python
all_snippets = collector.names()
print(f"Available snippets: {all_snippets}")
```

### `contains(name: str) -> bool`

Checks if a snippet with the given name exists in the collection.

**Parameters:**
- `name` (str): The name of the snippet to check

**Returns:**
- `bool`: `True` if the snippet exists, `False` otherwise

**Example:**
```python
if collector.contains("HelperFunction"):
    content = collector.get("HelperFunction")
```

### `size() -> int`

Returns the total number of snippets collected.

**Returns:**
- `int`: Number of snippets in the collection

**Example:**
```python
print(f"Found {collector.size()} snippets")
```

## String Representations

### `__str__() -> str`

Returns a concise string representation showing the directory and snippet count.

**Example output:**
```
Snippet(directory='/path/to/code', snippets=5)
```

### `__repr__() -> str`

Returns a detailed string representation including all snippet names.

**Example output:**
```
Snippet(directory='/path/to/code', snippets=['MyFunction', 'HelperClass', 'DataProcessor'])
```

## Snippet Format

Snippets in your source files should follow this format:

```python
# Regular code here

// snippet MyFunction
def my_function():
    return "Hello, World!"
// end snippet

# More code here

/* snippet HelperClass */
class Helper:
    def process(self, data):
        return data.upper()
/* end snippet */
```

## Supported Features

- **Recursive scanning**: Searches all subdirectories
- **Multiple file types**: Works with any text-based files
- **Flexible comment styles**: Supports `//`, `#`, `/* */`, and other comment formats
- **Case-insensitive keywords**: `snippet` and `end snippet` are matched case-insensitively
- **Identifier validation**: Snippet names must be valid identifiers (letters, digits, underscore)
- **Error handling**: Gracefully handles unreadable files and encoding issues
- **Duplicate detection**: Prevents duplicate snippet names and reports conflicts
- **Completeness validation**: Ensures all snippets have proper end markers

## Error Handling

The class includes robust error handling:

- **Missing directory**: Raises `ValueError` if the specified directory doesn't exist
- **Invalid directory**: Raises `ValueError` if the path is not a directory
- **Duplicate snippets**: Raises `ValueError` if the same snippet name appears multiple times
- **Unterminated snippets**: Raises `ValueError` if a snippet lacks an end marker
- **File access issues**: Silently skips files that cannot be read (binary files, permission issues)

## Usage Examples

### Basic Usage

```python
# Create collector and scan directory
collector = Snippet("./src")

# Check what was found
print(f"Found {collector.size()} snippets: {collector.names()}")

# Retrieve specific snippets
if collector.contains("DatabaseQuery"):
    query_code = collector.get("DatabaseQuery")
    print(query_code)
```

### Processing All Snippets

```python
collector = Snippet("./project")

# Process all snippets
for name in collector.names():
    content = collector.get(name)
    print(f"=== {name} ===")
    print(content)
    print()
```

### Conditional Usage

```python
collector = Snippet("./examples")

# Use snippets conditionally
required_snippets = ["Setup", "MainLoop", "Cleanup"]
missing = [name for name in required_snippets if not collector.contains(name)]

if missing:
    print(f"Missing required snippets: {missing}")
else:
    print("All required snippets found!")
```