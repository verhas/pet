import pytest
from pet.macros.counters import ChapterCounter


def test_first_chapter():
    c = ChapterCounter()
    assert c() == "# 1"


def test_increments():
    c = ChapterCounter()
    c()
    assert c() == "# 2"
    assert c() == "# 3"


def test_nested_section():
    c = ChapterCounter()
    c()      # # 1
    c.open()
    assert c() == "## 1.1"
    assert c() == "## 1.2"


def test_close_returns_to_parent():
    c = ChapterCounter()
    c()      # # 1
    c.open()
    c()      # ## 1.1
    c.close()
    assert c() == "# 2"


def test_three_levels():
    c = ChapterCounter()
    c()      # # 1
    c.open()
    c()      # ## 1.1
    c.open()
    assert c() == "### 1.1.1"


def test_reset():
    c = ChapterCounter()
    c()
    c()
    c.reset()
    assert c() == "# 1"


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
    c()
    assert c.get_current_numbers() == (1,)
    c.open()
    c()
    assert c.get_current_numbers() == (1, 1)


def test_chapter_alias():
    c = ChapterCounter()
    assert c() == c.chapter()[:2] + "1"


def test_composable_with_out(capsys):
    c = ChapterCounter()
    result = c()
    print(result, end='')
    assert capsys.readouterr().out == "# 1"
