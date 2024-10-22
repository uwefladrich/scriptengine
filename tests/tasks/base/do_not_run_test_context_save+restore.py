from scriptengine.context import Context

SAMPLE_CONTEXT = Context(
    {
        "foo": 0.1,
        "bar": {
            "a": [2, 3, 4, 5],
            "b": 6,
        },
        "baz": "seven",
    }
)


def test_context_save():
    assert False


def test_context_restore():
    assert False
