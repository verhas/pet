from pet.macros.transformer import Transformer


def test_basic_transform():
    t = Transformer(str.upper)
    assert t("hello") == "HELLO"


def test_lambda():
    t = Transformer(lambda s: s.replace("a", "b"))
    assert t("banana") == "bbnbnb"


def test_compose():
    strip = Transformer(str.strip)
    upper = Transformer(str.upper)
    combined = strip.compose(upper)
    assert combined("  hello  ") == "HELLO"


def test_compose_order():
    add_x = Transformer(lambda s: s + "x")
    upper = Transformer(str.upper)
    # apply add_x first, then upper
    combined = add_x.compose(upper)
    assert combined("a") == "AX"


def test_identity():
    t = Transformer(lambda s: s)
    assert t("anything") == "anything"
