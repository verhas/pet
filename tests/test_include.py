import pytest
from pet.macros.include import include


def test_returns_file_content(tmp_path):
    f = tmp_path / "hello.txt"
    f.write_text("line1\nline2\n")
    result = include(str(f))
    assert "line1" in result
    assert "line2" in result


def test_returns_exact_content(tmp_path):
    content = "Hello, World!\nSecond line."
    f = tmp_path / "test.txt"
    f.write_text(content)
    assert include(str(f)) == content


def test_missing_file_raises():
    with pytest.raises(FileNotFoundError):
        include("nonexistent_file_xyz_abc.txt")


def test_composable_with_upper(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("hello")
    assert include(str(f)).upper() == "HELLO"
