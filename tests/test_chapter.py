import pytest
from pet.macros.chapter import chapter


def test_first_chapter():
    c = chapter()
    assert c() == "# 1"


def test_increments():
    c = chapter()
    c()
    assert c() == "# 2"
    assert c() == "# 3"


def test_nested_section():
    c = chapter()
    c()      # # 1
    c.open()
    assert c() == "## 1.1"
    assert c() == "## 1.2"


def test_close_returns_to_parent():
    c = chapter()
    c()      # # 1
    c.open()
    c()      # ## 1.1
    c.close()
    assert c() == "# 2"


def test_three_levels():
    c = chapter()
    c()      # # 1
    c.open()
    c()      # ## 1.1
    c.open()
    assert c() == "### 1.1.1"


def test_reset():
    c = chapter()
    c()
    c()
    c.reset()
    assert c() == "# 1"


def test_close_at_root_raises():
    c = chapter()
    with pytest.raises(ValueError):
        c.close()


def test_get_current_level():
    c = chapter()
    assert c.get_current_level() == 1
    c.open()
    assert c.get_current_level() == 2
    c.close()
    assert c.get_current_level() == 1


def test_get_current_numbers():
    c = chapter()
    c()
    assert c.get_current_numbers() == (1,)
    c.open()
    c()
    assert c.get_current_numbers() == (1, 1)


def test_call_same_as_next():
    c1 = chapter()
    c2 = chapter()
    assert c1() == c2.next()


# --- header_prefix and sep ---------------------------------------------------

def test_custom_header_prefix():
    c = chapter(header_prefix="=")
    assert c() == "= 1"
    c.open()
    assert c() == "== 1.1"


def test_custom_sep():
    c = chapter(sep=": ")
    assert c() == "#: 1"
    c.open()
    assert c() == "##: 1.1"


def test_no_prefix_no_sep():
    c = chapter(header_prefix="", sep="")
    assert c() == "1"
    c.open()
    assert c() == "1.1"


def test_rst_style():
    # reStructuredText section markers are not repeated — header_prefix="" works
    c = chapter(header_prefix="", sep=" ")
    assert c() == " 1"


def test_custom_prefix_nested():
    c = chapter(header_prefix="*", sep=" - ")
    c()        # * - 1
    c.open()
    c()        # ** - 1.1
    c.close()
    assert c() == "* - 2"


def test_composable_with_out(capsys):
    c = chapter()
    result = c()
    print(result, end='')
    assert capsys.readouterr().out == "# 1"
