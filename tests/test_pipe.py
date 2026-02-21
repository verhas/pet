from pet.macros.pipe import pipe


def test_identity():
    assert pipe("anything") == "anything"


def test_basic_transform():
    assert (pipe | str.upper)("hello") == "HELLO"


def test_lambda():
    assert (pipe | (lambda s: s.replace("a", "b")))("banana") == "bbnbnb"


def test_pipe_chained():
    result = pipe | str.upper | str.strip
    assert result("  hello  ") == "HELLO"


def test_and_then_with_pipe_arg():
    strip = pipe | str.strip
    result = strip.and_then(pipe | str.upper)
    assert result("  hello  ") == "HELLO"


def test_and_then_order():
    add_x = pipe | (lambda s: s + "x")
    result = add_x.and_then(str.upper)
    assert result("a") == "AX"


def test_and_then_returns_callable():
    result = (pipe | str.upper).and_then(str.lower)
    assert callable(result)


def test_and_then_applies_self_first():
    add_x = pipe | (lambda s: s + "x")
    result = add_x.and_then(lambda s: s + "y")
    assert result("a") == "axy"


def test_and_then_self_applied_once():
    calls = []
    def counting(s):
        calls.append(s)
        return s + "!"
    (pipe | counting).and_then(lambda s: s)("x")
    assert len(calls) == 1


def test_and_then_chained():
    result = (pipe | (lambda s: s + "1")).and_then(lambda s: s + "2").and_then(lambda s: s + "3")
    assert result("a") == "a123"


def test_pipe_operator_order():
    result = pipe | (lambda s: s + "x") | str.upper
    assert result("a") == "AX"


def test_pipe_operator_chained():
    result = pipe | (lambda s: s + "1") | (lambda s: s + "2") | (lambda s: s + "3")
    assert result("a") == "a123"


def test_pipe_operator_equivalent_to_and_then():
    add_x = pipe | (lambda s: s + "x")
    assert (add_x | (lambda s: s + "y"))("a") == add_x.and_then(lambda s: s + "y")("a")


def test_on_lines_applies_to_each_line():
    strip = (pipe | str.strip).on_lines()
    assert strip("  hello  \n  world  ") == "hello\nworld"


def test_on_lines_returns_callable():
    result = (pipe | str.upper).on_lines()
    assert callable(result)


def test_on_lines_multiline():
    upper = (pipe | str.upper).on_lines()
    assert upper("hello\nworld") == "HELLO\nWORLD"


def test_on_lines_composed():
    result = (pipe | str.strip).on_lines() | (lambda s: s.replace("\n", ", "))
    assert result("  a  \n  b  \n  c  ") == "a, b, c"


def test_pipe_is_reusable():
    # pipe itself is never mutated; each | creates a new Pipe
    upper = pipe | str.upper
    lower = pipe | str.lower
    assert upper("hello") == "HELLO"
    assert lower("HELLO") == "hello"
    assert pipe("unchanged") == "unchanged"


def test_dedent_number_composition():
    from pet.macros.dedent import dedent
    from pet.macros.number import number
    result = pipe | dedent | number(fmt="{:2d} ")
    assert result("    hello\n    world") == " 1 hello\n 2 world"
