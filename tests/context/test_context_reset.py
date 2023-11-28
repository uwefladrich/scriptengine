from scriptengine.context import Context


def test_reset_all():
    c = Context(
        foo=0.1,
        bar={
            "a": [2, 3, 4, 5],
            "b": 6,
        },
        bam="seven",
    )
    c.reset()
    assert c == dict()


def test_reset_keep():
    c = Context(
        foo=0.1,
        bar={
            "a": [2, 3, 4, 5],
            "b": 6,
        },
        bam="seven",
    )
    c.reset(keep=["foo"])
    assert c == dict(foo=0.1)


def test_reset_keep_nested():
    c = Context(
        foo=0.1,
        bar={
            "a": [2, 3, 4, 5],
            "b": 6,
        },
        bam="seven",
    )
    c.reset(keep=["bar.b"])
    assert c == dict(bar={"b": 6})


def test_reset_keep_list():
    c = Context(
        foo=0.1,
        bar={
            "a": [2, 3, 4, 5],
            "b": 6,
        },
        bam="seven",
    )
    c.reset(keep=["foo", "bar.b"])
    assert c == dict(foo=0.1, bar={"b": 6})
