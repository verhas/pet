import pytest
from pathlib import Path
from pet.processor import process_template

ROOT = Path(__file__).parent.parent
FIXTURES = ROOT / "tests" / "snippet"


def test_simple_print(tmp_path, monkeypatch):
    monkeypatch.chdir(ROOT)
    t = tmp_path / "in.pet"
    t.write_text("Hello {% print('World') %}!")
    out = tmp_path / "out.txt"
    process_template(str(t), str(out))
    assert out.read_text() == "Hello World\n!"


def test_variable_persists_across_blocks(tmp_path, monkeypatch):
    monkeypatch.chdir(ROOT)
    t = tmp_path / "in.pet"
    t.write_text("{% x = 42 %}Value: {% print(x) %}")
    out = tmp_path / "out.txt"
    process_template(str(t), str(out))
    assert out.read_text() == "Value: 42\n"


def test_verbatim_text_preserved(tmp_path, monkeypatch):
    monkeypatch.chdir(ROOT)
    t = tmp_path / "in.pet"
    t.write_text("# Title\n\nSome text with no code blocks.")
    out = tmp_path / "out.txt"
    process_template(str(t), str(out))
    assert out.read_text() == "# Title\n\nSome text with no code blocks."


def test_error_in_code_block_becomes_comment(tmp_path, monkeypatch):
    monkeypatch.chdir(ROOT)
    t = tmp_path / "in.pet"
    t.write_text("Before {% raise ValueError('oops') %} After")
    out = tmp_path / "out.txt"
    process_template(str(t), str(out))
    content = out.read_text()
    assert "ERROR" in content
    assert "Before" in content
    assert "After" in content


def test_missing_input_exits(tmp_path):
    with pytest.raises(SystemExit):
        process_template("no_such_file.pet", str(tmp_path / "out.txt"))


def test_snippet_integration(tmp_path, monkeypatch):
    monkeypatch.chdir(ROOT)
    out = tmp_path / "output.md"
    process_template(str(FIXTURES / "snippet_test.md.pet"), str(out))
    content = out.read_text()
    assert "Snip.pet Demonstration" in content
    assert "this is a sample snip.pet content" in content
