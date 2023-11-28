import yaml

from scriptengine.context import Context

SAMPLE_YAML = """
foo: 0.1
bar:
  a: [2, 3, 4, 5]
  b: 7
baz: 'eight'
"""

SAMPLE_DICT = yaml.safe_load(SAMPLE_YAML)


def test_load(tmp_path):
    c = Context()
    yaml_file = tmp_path / "fload.yml"
    yaml_file.write_text(SAMPLE_YAML)
    with open(yaml_file) as f:
        c.load(f)
    assert c == SAMPLE_DICT


def test_save(tmp_path):
    c = Context(SAMPLE_DICT)
    yaml_file = tmp_path / "fsave.yml"
    with open(yaml_file, "w") as f:
        c.save(f)
    with open(yaml_file) as f:
        assert yaml.safe_load(f) == SAMPLE_DICT
