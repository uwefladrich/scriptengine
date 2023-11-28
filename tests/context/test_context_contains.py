from scriptengine.context import Context


def test_context_contains_simple():
    c = Context({"foo": {"bar": 1}})
    assert "foo" in c
    assert "bar" in c["foo"]
    assert "fox" not in c
    assert 1 not in c



def test_context_contains_nested():
    c = Context({"foo": {"bar": 1}})
    assert "foo" in c
    assert "foo.bar" in c
    assert "foo.bam" not in c
