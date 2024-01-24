from warnings import filterwarnings

from public import public


@public
class InvalidMetadata(UserWarning):
    pass


filterwarnings('always', category=InvalidMetadata)
