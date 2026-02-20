import io
import pytest
from contextlib import redirect_stdout
from pet.macros.counters import ChapterCounter


def output(fn):
    buf = io.StringIO()
    with redirect_stdout(buf):
        fn()
    return buf.getvalue()


def test_first_chapter():
    c = ChapterCounter()
    assert output(c) == "# 1"


def test_increments():
    c = ChapterCounter()
    output(c)
    assert output(c) == "# 2"
    assert output(c) == "# 3"


def test_nested_section():
    c = ChapterCounter()
    output(c)      # # 1
    c.open()
    assert output(c) == "## 1.1"
    assert output(c) == "## 1.2"


def test_close_returns_to_parent():
    c = ChapterCounter()
    output(c)      # # 1
    c.open()
    output(c)      # ## 1.1
    c.close()
    assert output(c) == "# 2"


def test_three_levels():
    c = ChapterCounter()
    output(c)      # # 1
    c.open()
    output(c)      # ## 1.1
    c.open()
    assert output(c) == "### 1.1.1"


def test_reset():
    c = ChapterCounter()
    output(c)
    output(c)
    c.reset()
    assert output(c) == "# 1"


def test_close_at_root_raises():
    c = ChapterCounter()
    with pytest.raises(ValueError):
        c.close()


def test_get_current_level():
    c = ChapterCounter()
    assert c.get_current_level() == 1
    c.open()
    assert c.get_current_level() == 2
    c.close()
    assert c.get_current_level() == 1


def test_get_current_numbers():
    c = ChapterCounter()
    output(c)
    assert c.get_current_numbers() == (1,)
    c.open()
    output(c)
    assert c.get_current_numbers() == (1, 1)


def test_chapter_alias():
    c = ChapterCounter()
    assert output(c.chapter) == output(ChapterCounter())
