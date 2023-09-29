from scriptengine.context import Context


def test_simple_update():
    c = Context({"foo": 1, "bar": 2})
    c.update({"bar": 3})
    assert c == {"foo": 1, "bar": 3}
