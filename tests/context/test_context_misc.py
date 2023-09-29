from scriptengine.context import Context


def test_set_with_integer_as_string_key():
    c = Context()
    c["1"] = 1
    assert c["1"] == 1


def test_overwrite_existing_key():
    c = Context()
    c["a.b"] = 1
    c["a.b.c"] = 1
    assert c["a.b.c"] == 1
    assert c["a"]["b"]["c"] == 1


def test_extend_dict():
    c = Context()
    c["a.b.c"] = 1
    c["a.b.d"] = 2
    assert c["a"]["b"]["c"] == 1
    assert c["a"]["b"]["d"] == 2
