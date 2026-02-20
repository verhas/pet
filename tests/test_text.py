from pet.macros.text import text


def test_prints_stored_text(capsys):
    t = text("hello")
    t()
    assert capsys.readouterr().out == "hello"


def test_no_trailing_newline(capsys):
    t = text("world")
    t()
    assert capsys.readouterr().out == "world"


def test_callable_multiple_times(capsys):
    t = text("x")
    t()
    t()
    assert capsys.readouterr().out == "xx"


def test_empty_string(capsys):
    t = text("")
    t()
    assert capsys.readouterr().out == ""


def test_multiline(capsys):
    t = text("line1\nline2")
    t()
    assert capsys.readouterr().out == "line1\nline2"
