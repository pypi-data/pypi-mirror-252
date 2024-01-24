from typing import NamedTuple
from enum import Enum

from public import public


@public
class Languages(Enum):
    js = 'javascript'
    py = 'python'
    rs = 'rust'

    def __str__(self):
        return self.name

    def upper(self):
        return self.name.upper()


@public
class Lang(NamedTuple):
    name: str
    attr: str
    manifest_file: str


langs = {
    Languages.js: Lang('javascript', 'js', 'package.json'),
    Languages.py: Lang('python', 'py', 'pyproject.toml'),
    Languages.rs: Lang('rust', 'rs', 'Cargo.toml'),
}
