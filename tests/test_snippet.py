import pytest
from pet.macros.snippet import Snippet

FIXTURES_DIR = "tests/snippet"


def test_finds_snippet_in_existing_fixture():
    s = Snippet(FIXTURES_DIR)
    assert s.contains("sample")
    assert "this is a sample snip.pet content" in s.get("sample")


def test_finds_snippet(tmp_path):
    (tmp_path / "code.c").write_text("// snippet hello\nworld\n// end snippet\n")
    s = Snippet(str(tmp_path))
    assert s.contains("hello")
    assert s.get("hello") == "world\n"


def test_size_and_names(tmp_path):
    (tmp_path / "code.py").write_text(
        "# snippet foo\nbar\n# end snippet\n"
        "# snippet baz\nqux\n# end snippet\n"
    )
    s = Snippet(str(tmp_path))
    assert s.size() == 2
    assert set(s.names()) == {"foo", "baz"}


def test_get_returns_none_for_missing(tmp_path):
    assert Snippet(str(tmp_path)).get("missing") is None


def test_contains_false(tmp_path):
    assert not Snippet(str(tmp_path)).contains("nonexistent")


def test_invalid_directory():
    with pytest.raises(ValueError):
        Snippet("/nonexistent/path/xyz")


def test_not_a_directory(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("hello")
    with pytest.raises(ValueError):
        Snippet(str(f))


def test_duplicate_snippet(tmp_path):
    (tmp_path / "code.py").write_text(
        "# snippet foo\nbar\n# end snippet\n"
        "# snippet foo\nbaz\n# end snippet\n"
    )
    with pytest.raises(ValueError, match="already exists"):
        Snippet(str(tmp_path))


def test_unterminated_snippet(tmp_path):
    (tmp_path / "code.py").write_text("# snippet foo\nbar\n")
    with pytest.raises(ValueError, match="not terminated"):
        Snippet(str(tmp_path))


def test_call_prints_snippet(tmp_path, capsys):
    (tmp_path / "code.py").write_text("# snippet hi\nhello\n# end snippet\n")
    s = Snippet(str(tmp_path))
    s("hi")
    assert "hello" in capsys.readouterr().out


def test_str_and_repr(tmp_path):
    s = Snippet(str(tmp_path))
    assert "Snippet" in str(s)
    assert "Snippet" in repr(s)
