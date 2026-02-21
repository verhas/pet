from pet.macros.dedent import dedent


def test_removes_common_indent():
    assert dedent("    hello\n    world") == "hello\nworld"


def test_preserves_relative_indent():
    assert dedent("    def foo():\n        return 42") == "def foo():\n    return 42"


def test_strips_trailing_spaces():
    assert dedent("    hello   \n    world   ") == "hello\nworld"


def test_leading_and_trailing_blank_lines_stripped():
    assert dedent("\n    hello\n    world\n") == "hello\nworld"


def test_triple_quoted_style():
    result = dedent("""
            def foo():
                return 42
            """)
    assert result == "def foo():\n    return 42"


def test_empty_lines_in_middle_preserved():
    assert dedent("    hello\n\n    world") == "hello\n\nworld"


def test_no_common_indent():
    assert dedent("hello\nworld") == "hello\nworld"


def test_partial_indent_uses_minimum():
    # "  b" has the smallest indent (2), so 2 spaces removed from all lines
    assert dedent("    a\n  b\n      c") == "  a\nb\n    c"


def test_composable_with_pipe():
    from pet.macros.pipe import pipe
    result = pipe | dedent
    assert result("    hello\n    world") == "hello\nworld"


def test_composable_with_pipe_operator():
    from pet.macros.pipe import pipe
    result = pipe | dedent | str.upper
    assert result("    hello\n    world") == "HELLO\nWORLD"
