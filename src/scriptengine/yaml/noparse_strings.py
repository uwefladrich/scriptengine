class NoParseYamlString(str):
    """This represents a string that should not be YAML-parsed"""


class NoParseJinjaString(str):
    """This represents a string that should not be parsed with Jinja2"""


class NoParseString(NoParseYamlString, NoParseJinjaString):
    """This represents a string that should not be parsed at all, neither YAML
    or Jinja2"""
