import yaml

from scriptengine.context import Context
from scriptengine.yaml.parser import parse


def from_yaml(string):
    return parse(yaml.load(string, Loader=yaml.FullLoader))


def test_find_basic(tmp_path):

    subdir = tmp_path / "foo"
    subdir.mkdir()

    (tmp_path / "bar-0.txt").touch()
    (subdir / "bar-1.txt").touch()
    (subdir / "bar-2.txt").touch()

    t = from_yaml(
        f"""
        base.find:
            path: {tmp_path}
            pattern: 'bar-?.txt'
        """
    )
    ctx = t.run(Context())
    assert set(ctx["result"]) == {
        f"{tmp_path}/bar-0.txt",
        f"{subdir}/bar-1.txt",
        f"{subdir}/bar-2.txt",
    }

    t = from_yaml(
        f"""
        base.find:
            path: {subdir}
            pattern: 'bar-?.txt'
        """
    )
    ctx = t.run(Context())
    assert set(ctx["result"]) == {
        f"{subdir}/bar-1.txt",
        f"{subdir}/bar-2.txt",
    }


def test_find_with_set(tmp_path):

    subdir = tmp_path / "foo"
    subdir.mkdir()

    (subdir / "bar-1.txt").touch()
    (subdir / "bar-2.txt").touch()

    t = from_yaml(
        f"""
        base.find:
            path: {subdir}
            pattern: 'bar-?.txt'
            set: foobar
        """
    )
    ctx = t.run(Context())
    assert set(ctx["foobar"]) == {
        f"{subdir}/bar-1.txt",
        f"{subdir}/bar-2.txt",
    }


def test_find_with_depth(tmp_path):

    subdir = tmp_path / "foo" / "foo_2"
    subdir.mkdir(parents=True)

    (subdir / "bar-1.txt").touch()
    (subdir / "bar-2.txt").touch()

    t = from_yaml(
        f"""
        base.find:
            path: {tmp_path}
            pattern: 'bar-?.txt'
            depth: 1
        """
    )
    ctx = t.run(Context())
    assert ctx["result"] == []


def test_find_with_file_type(tmp_path):

    subdir = tmp_path / "foo"
    subdir.mkdir()

    (subdir / "bar-1.txt").touch()
    (subdir / "bar-2.txt").mkdir()

    t = from_yaml(
        f"""
        base.find:
            path: {subdir}
            pattern: 'bar-?.txt'
        """
    )
    ctx = t.run(Context())
    assert set(ctx["result"]) == {
        f"{subdir}/bar-1.txt",
    }

    t = from_yaml(
        f"""
        base.find:
            path: {subdir}
            pattern: 'bar-?.txt'
            type: dir
        """
    )
    ctx = t.run(Context())
    assert set(ctx["result"]) == {
        f"{subdir}/bar-2.txt",
    }
