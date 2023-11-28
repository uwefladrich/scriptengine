from scriptengine.context import Context


def test_context_create_from_nothing():
    c = Context()
    assert type(c) == Context
    assert c == {}


def test_context_create_from_empty():
    c = Context({})
    assert type(c) == Context
    assert c == {}


def test_context_create_from_nonempty():
    c = Context({"foo": {"bar": 1}})
    assert type(c) == Context
    assert c == {"foo": {"bar": 1}}
