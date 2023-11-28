import pytest

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


def test_set_nested_dotted_keys():
    dotted_dict = {"f1": {"g1.h1": 1, "g2": {"h2.i1": 2}}}
    expanded_dict = {"f1": {"g1": {"h1": 1}, "g2": {"h2": {"i1": 2}}}}
    c = Context(dotted_dict)
    assert c == expanded_dict


def test_set_int_key():
    c = Context()
    c[1] = "foo"
    assert c[1] == "foo"


def test_mixed_access():
    c = Context({"foo": {"bar": {"baz": 1}}})
    assert c["foo.bar"]["baz"] == 1


def test_too_many_dots():
    c = Context({"foo": {"bar": 1}})
    with pytest.raises(KeyError):
        c["foo.bar.baz"]


def test_wrong_key_type():
    c = Context({"foo": {"bar": 1}})
    with pytest.raises(KeyError):
        c[1]


def test_add_wrong_type():
    with pytest.raises(TypeError):
        Context() + 1
