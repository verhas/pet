from pathlib import Path
from pet.processor import process_template

ROOT = Path(__file__).parent.parent
TEMPLATE = ROOT / "tests" / "chapter" / "test.md.pet"
EXPECTED = ROOT / "tests" / "chapter" / "test.md"


def test_chapter_template_output(tmp_path, monkeypatch):
    monkeypatch.chdir(ROOT)
    out = tmp_path / "result.md"
    process_template(str(TEMPLATE), str(out))
    assert out.read_text() == EXPECTED.read_text()
