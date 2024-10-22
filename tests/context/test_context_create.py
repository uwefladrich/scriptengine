from scriptengine.context import Context


def test_context_create_from_nothing():
    c = Context()
    assert isinstance(c, Context)
    assert c == {}


def test_context_create_from_empty():
    c = Context({})
    assert isinstance(c, Context)
    assert c == {}


def test_context_create_from_nonempty():
    c = Context({"foo": {"bar": 1}})
    assert isinstance(c, Context)
    assert c == {"foo": {"bar": 1}}
