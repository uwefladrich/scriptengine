from scriptengine.context import Context


def test_get_by_dotted_key_simple():
    c = Context({"foo": {"bar": 1}})
    assert c["foo.bar"] == 1


def test_get_by_dotted_key_nested():
    c = Context({"foo": {"bar": {"baz": 1}}})
    assert c["foo.bar.baz"] == 1


def test_set_dotted_key():
    c = Context()
    c["foo.bar"] = 1
    assert c["foo.bar"] == 1
    assert c["foo"]["bar"] == 1


def test_mixed_access():
    c = Context({"foo": {"bar": {"baz": 1}}})
    assert c["foo.bar"]["baz"] == 1
