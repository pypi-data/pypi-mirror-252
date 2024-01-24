from urllib3.util import Url as _Url, parse_url
from omniblack.model import ValidationResult, ModelType


class Url(ModelType):
    implmentaion = _Url

    def from_string(self, string: str):
        return parse_url(string)

    def to_string(self, value: _Url):
        return value.url

    def validator(self, value, path):
        messages = []

        return ValidationResult(not messages, messages)

    def json_schema(self):
        return {
            'type': 'string',
            'format': 'iri',
        }
