import re

from packaging.version import VERSION_PATTERN
from omniblack.model import ValidationResult, ModelType
from ..version import Version as VersionImpl


def unverbosify_regex_simple(verbose):
    WS_RX = r'(?<!\\)((\\{2})*)\s+'
    CM_RX = r'(?<!\\)((\\{2})*)#.*$(?m)'

    return re.sub(WS_RX, "\\1", re.sub(CM_RX, "\\1", verbose))


class Version(ModelType):
    implmentation = VersionImpl

    def to_string(self, version):
        return str(version)

    def from_string(self, string):
        return self.implmentation(string)

    def validator(self, value, path):
        return ValidationResult(True, tuple())

    def json_schema(self):
        pattern = unverbosify_regex_simple(VERSION_PATTERN)
        return {
            'type': 'string',
            'pattern': f'^{pattern}$',
        }
