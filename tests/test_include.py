from pet.macros.include import include


def test_includes_file_content(tmp_path, capsys):
    f = tmp_path / "hello.txt"
    f.write_text("line1\nline2\n")
    include(str(f))
    out = capsys.readouterr().out
    assert "line1" in out
    assert "line2" in out


def test_preserves_content_exactly(tmp_path, capsys):
    content = "Hello, World!\nSecond line."
    f = tmp_path / "test.txt"
    f.write_text(content)
    include(str(f))
    out = capsys.readouterr().out
    assert "Hello, World!" in out
    assert "Second line." in out


def test_missing_file_prints_error(capsys):
    include("nonexistent_file_xyz_abc.txt")
    out = capsys.readouterr().out
    assert "Error" in out
    assert "nonexistent_file_xyz_abc.txt" in out
