import re


def include(filename):
    """
    Reads a file and prints lines.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        print("".join(lines))
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
