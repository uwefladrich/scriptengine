from deepdiff import Delta

from scriptengine.context import Context, ContextUpdate


def test_create_empty_context_update():
    cu = ContextUpdate()
    assert type(cu) is ContextUpdate


def test_create_merge_context_update():
    d = {"foo": 1}
    cu = ContextUpdate(d)
    assert type(cu) is ContextUpdate
    assert cu.merge == d
    assert cu.delta is None


def test_create_delta():
    d1 = {"foo": 1}
    d2 = {"bar": 2}
    cu = ContextUpdate(d1, d2)
    assert type(cu) is ContextUpdate
    assert cu.merge is None
    assert type(cu.delta) is Delta
    assert d1 + cu.delta == d2


def test_context_update_empty():
    d = {"foo": 1}
    c = Context(d)
    cu = ContextUpdate()
    assert c + cu == d


def test_context_update_delta_adds():
    d1 = {"foo": 1}
    d2 = {"foo": 1, "bar": 2}
    c = Context(d1)
    cu = ContextUpdate(d1, d2)
    assert c + cu == {"foo": 1, "bar": 2}


def test_context_update_delta_removes():
    d1 = {"foo": 1}
    d2 = {"bar": 2}
    c = Context(d1)
    cu = ContextUpdate(d1, d2)
    assert c + cu == {"bar": 2}


def test_context_update_merge_appends():
    d1 = {"foo": [1, 2]}
    d2 = {"foo": [3, 4]}
    c = Context(d1)
    cu = ContextUpdate(d2)
    assert c + cu == {"foo": [1, 2, 3, 4]}
