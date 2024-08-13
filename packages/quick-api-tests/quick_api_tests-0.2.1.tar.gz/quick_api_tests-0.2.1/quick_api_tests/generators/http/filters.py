import re
import pytest


def to_snake_case(string):
    if isinstance(string, str):
        string = string.replace(" ", "_").replace("/", "_").replace(".", "_")
        string = string.replace("{", "").replace("}", "")
        string = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", string)
        string = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", string)
        string = string.replace("-", "_").lower().strip("_")
        return string


def to_camel_case(string):
    if isinstance(string, str):
        words = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", string)
        camel_case_words = [word.capitalize() for word in words]
        camel_case_title = "".join(camel_case_words)
        return camel_case_title
