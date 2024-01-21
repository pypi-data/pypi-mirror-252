from re import compile
from .languages import Languages

unscoped_name = '(?P<name>[a-z][a-z_-]{0,200}[a-z])'

unscoped_name_re = compile(unscoped_name)

py_name_re = compile(rf'omniblack\.{unscoped_name}')

js_name_re = compile(f'@omniblack/{unscoped_name}')

rs_name_re = unscoped_name_re

regexes = (
    unscoped_name_re,
    py_name_re,
    js_name_re,
    rs_name_re,
)


def is_valid_unscoped_name(name):
    return bool(unscoped_name_re.fullmatch(name))


def get_unscoped_name(name):
    for regex in regexes:
        match = regex.fullmatch(name)
        if match:
            return match['name']
    else:
        raise TypeError(
            f'{name} is not a valid package name.',
        )


def canonicalize_name(name, lang):
    match lang:
        case Languages.py if py_name_re.fullmatch(name):
            return name
        case Languages.js if match := js_name_re.fullmatch(name):
            unscoped_name = match['name']
            return f'omniblack.{unscoped_name}'
        case Languages.rs if match := rs_name_re.fullmatch(name):
            unscoped_name = match['name']
            return f'omniblack.{unscoped_name}'
        case _:
            raise ValueError(
                f'{name} is not a valid omniblack package name',
                name,
            )
