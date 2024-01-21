from omniblack.model import Model
from .url import Url
from .version import Version

model = Model(
    'Omniblack Repo',
    struct_packages=['omniblack.repo.model'],
    types=[Url, Version],
)
