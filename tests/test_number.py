from pet.macros.number import number


def test_single_line():
    n = number()
    assert n("hello") == "1 hello"


def test_multiline():
    n = number()
    assert n("""
line1
line2
line3
    """) == "1 line1\n2 line2\n3 line3"


def test_counter_persists_across_calls():
    n = number()
    n("line1\nline2")
    assert n("line3") == "3 line3"


def test_step():
    n = number(step=2)
    assert n("a\nb\nc") == "1 a\n3 b\n5 c"


def test_negative_step():
    n = number(start=5, step=-1)
    assert n("a\nb\nc") == "5 a\n4 b\n3 c"


def test_custom_format_zero_padded():
    n = number(fmt="{:03d} ")
    assert n("a\nb") == "001 a\n002 b"


def test_custom_format_right_aligned():
    n = number(fmt="{:4d} ")
    assert n("a\nb") == "   1 a\n   2 b"


def test_custom_format_hex():
    n = number(start=10, fmt="{:x} ")
    assert n("a\nb") == "a a\nb b"


def test_trailing_newline_stripped():
    n = number()
    assert n("line1\nline2\n") == "1 line1\n2 line2"


def test_empty_line_gets_number_only():
    n = number()
    assert n("a\n\nb") == "1 a\n2\n3 b"


def test_restart_by_creating_new_instance():
    n = number()
    n("a\nb")
    n = number()
    assert n("c") == "1 c"


def test_custom_start():
    n = number(start=10)
    assert n("a\nb") == "10 a\n11 b"
