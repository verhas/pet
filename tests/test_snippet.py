import pytest
from pet.macros.snippet import snippet

FIXTURES_DIR = "tests/snippet"


def test_finds_snippet_in_existing_fixture():
    s = snippet(FIXTURES_DIR)
    assert s.contains("sample")
    assert "this is a sample snip.pet content" in s.get("sample")


def test_finds_snippet(tmp_path):
    (tmp_path / "code.c").write_text("// snippet hello\nworld\n// end snippet\n")
    s = snippet(str(tmp_path))
    assert s.contains("hello")
    assert s.get("hello") == "world\n"


def test_size_and_names(tmp_path):
    (tmp_path / "code.py").write_text(
        "# snippet foo\nbar\n# end snippet\n"
        "# snippet baz\nqux\n# end snippet\n"
    )
    s = snippet(str(tmp_path))
    assert s.size() == 2
    assert set(s.names()) == {"foo", "baz"}


def test_get_returns_none_for_missing(tmp_path):
    assert snippet(str(tmp_path)).get("missing") is None


def test_contains_false(tmp_path):
    assert not snippet(str(tmp_path)).contains("nonexistent")


def test_nonexistent_glob_yields_no_snippets():
    # A glob that matches nothing is not an error — just no snippets found
    s = snippet("/nonexistent/path/xyz/*.py")
    assert s.size() == 0


def test_glob_pattern(tmp_path):
    (tmp_path / "a.py").write_text("# snippet alpha\nAAA\n# end snippet\n")
    (tmp_path / "b.txt").write_text("# snippet beta\nBBB\n# end snippet\n")
    s = snippet(str(tmp_path / "*.py"))
    assert s.contains("alpha")
    assert not s.contains("beta")


def test_list_of_sources(tmp_path):
    d1 = tmp_path / "src"
    d2 = tmp_path / "lib"
    d1.mkdir()
    d2.mkdir()
    (d1 / "a.py").write_text("# snippet foo\nFOO\n# end snippet\n")
    (d2 / "b.py").write_text("# snippet bar\nBAR\n# end snippet\n")
    s = snippet([str(d1), str(d2)])
    assert s.contains("foo")
    assert s.contains("bar")


def test_list_of_globs(tmp_path):
    (tmp_path / "a.py").write_text("# snippet pysnip\nPY\n# end snippet\n")
    (tmp_path / "b.js").write_text("// snippet jssnip\nJS\n// end snippet\n")
    (tmp_path / "c.txt").write_text("# snippet txtsnip\nTXT\n# end snippet\n")
    s = snippet([str(tmp_path / "*.py"), str(tmp_path / "*.js")])
    assert s.contains("pysnip")
    assert s.contains("jssnip")
    assert not s.contains("txtsnip")


def test_deduplication(tmp_path):
    # Same directory listed twice — snippets should appear only once
    (tmp_path / "code.py").write_text("# snippet dup\nhello\n# end snippet\n")
    s = snippet([str(tmp_path), str(tmp_path)])
    assert s.size() == 1


def test_duplicate_snippet(tmp_path):
    (tmp_path / "code.py").write_text(
        "# snippet foo\nbar\n# end snippet\n"
        "# snippet foo\nbaz\n# end snippet\n"
    )
    with pytest.raises(ValueError, match="already exists"):
        snippet(str(tmp_path))


def test_unterminated_snippet(tmp_path):
    (tmp_path / "code.py").write_text("# snippet foo\nbar\n")
    with pytest.raises(ValueError, match="not terminated"):
        snippet(str(tmp_path))


def test_call_returns_snippet(tmp_path):
    (tmp_path / "code.py").write_text("# snippet hi\nhello\n# end snippet\n")
    s = snippet(str(tmp_path))
    assert "hello" in s("hi")


def test_str_returns_empty(tmp_path):
    # __str__ returns '' — container convention in PET
    assert str(snippet(str(tmp_path))) == ''


def test_repr(tmp_path):
    s = snippet(str(tmp_path))
    assert "snippet" in repr(s)


def test_exclude_glob(tmp_path):
    (tmp_path / "keep.py").write_text("# snippet kept\nyes\n# end snippet\n")
    (tmp_path / "skip.md").write_text("# snippet skipped\nno\n# end snippet\n")
    s = snippet(str(tmp_path), exclude="*.md")
    assert s.contains("kept")
    assert not s.contains("skipped")
