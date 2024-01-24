from ruamel.yaml import YAML as _YAML
from public import public

from omniblack.utils import Enum

from .version import Version


@public
class YAML(_YAML):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.register_class(Version)
        self.register_class(Enum)
        Enum.set_yaml(self)
