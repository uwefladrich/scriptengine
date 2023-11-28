import pytest

from scriptengine.context import Context


def test_merge_new_key():
    c = Context({"foo": {"bar": 1}})
    c.merge({"foo": {"baz": 2}})
    assert c == {"foo": {"bar": 1, "baz": 2}}


def test_merge_existing_key_1():
    c = Context({"foo": {"bar": 1}})
    c.merge({"foo": {"bar": 2}})
    assert c == {"foo": {"bar": 2}}


def test_merge_existing_key_2():
    c = Context({"foo": {"bar": 1, "baz": 2}})
    c.merge({"foo": {"baz": 3}})
    assert c == {"foo": {"bar": 1, "baz": 3}}


def test_merge_existing_key_3():
    c = Context({"foo": {"bar": 1, "baz": 2}})
    c.merge({"foo": {"bar": {"bam": 3}}})
    assert c == {"foo": {"bar": {"bam": 3}, "baz": 2}}


def test_merge_list():
    c = Context({"foo": [1, 2, 3]})
    c.merge({"foo": [4, 5]})
    assert c["foo"] == [1, 2, 3, 4, 5]


def test_merge_raises_typerror():
    c = Context({"foo": 1})
    with pytest.raises(TypeError):
        c.merge(1)


def test_merge_with_add():
    c = Context({"foo": 1, "bar": 2})
    c += {"bar": 3, "baz": 4}
    assert c == {"foo": 1, "bar": 3, "baz": 4}


def test_merge_with_context():
    c1 = Context({"foo": 1, "bar": 2})
    c2 = Context({"bar": 3, "baz": 4})
    c1.merge(c2)
    assert c1 == {"foo": 1, "bar": 3, "baz": 4}


def test_merge_add_with_context():
    c = Context({"foo": 1, "bar": 2})
    c.merge(Context({"bar": 3, "baz": 4}))
    assert c == {"foo": 1, "bar": 3, "baz": 4}
