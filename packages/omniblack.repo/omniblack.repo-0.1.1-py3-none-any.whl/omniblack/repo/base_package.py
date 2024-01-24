import json
from itertools import islice
from contextlib import suppress
from logging import getLogger
from typing import Optional
from collections.abc import Mapping
from warnings import warn
from operator import attrgetter
from os import PathLike, fspath
from functools import partial
from os.path import (
    join,
    isdir as is_dir,
    basename as base_name,
    relpath as relative_path,
    dirname,
    exists,
)

import tomlkit as toml
from dataclasses import dataclass
from public import public
from fs.base import FS
from fs.errors import DirectoryExists
from fs.path import (
    combine,
    relpath,
    isparent,
    recursepath,
    abspath,
)


from .model import model
from .package_group import PackageGroup
from .metadata_warning import InvalidMetadata
from .names import is_valid_unscoped_name
from .version import Version
from .find_root import find_root
from .tree import build_tree
from .languages import Languages
from .package_info import (
    JsPackageInfo,
    PyPackageInfo,
    RsPackageInfo,
    PackageInfo,
)

log = getLogger(__name__)


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(islice(iterable, n))


class TomlParseError(ValueError):
    """
    Used to indicate we couldn't parse a toml file.
    See the cause error to see a detailed syntax error.
    """


# In priority order
package_suffixes = ('yaml', 'yml', 'toml', 'json5', 'json')

possible_packages_configs = tuple(
    f'package_config.{suffix}'
    for suffix in package_suffixes
)


def get_source_dir(pkg_path: PathLike):
    omniblack_pkg = join(pkg_path, 'omniblack', base_name(pkg_path))
    py_src_pkg = join(pkg_path, 'src', 'omniblack', base_name(pkg_path))

    if exists(omniblack_pkg):
        return omniblack_pkg
    elif exists(py_src_pkg):
        return py_src_pkg
    else:
        return join(pkg_path, 'src')


class lang_func:
    def __new__(cls, impl, lang=None):
        if lang is None:
            return partial(cls, lang=impl)
        else:
            return super().__new__(cls)

    def __init__(self, impl, lang=None):
        self.__impls = {lang: impl}
        self.__wrapped__ = impl

    def __call__(self, impl, lang=None):
        if lang is None:
            return partial(self.__call__, lang=impl)
        else:
            self.__impls[lang] = impl
            return self

    def __call_impl(self, lang, *args, owner, **kwargs):
        return self.__impls[lang](owner, *args, **kwargs)

    def __get__(self, instance, owner=None):
        return partial(self.__call_impl, owner=owner)


@public
@dataclass
class Package:
    name: str
    version: Version
    path: str
    rel_path: str
    src_dir: str
    root_dir: str

    config: Mapping
    config_path: str

    languages: dict[str, PackageInfo]
    js: Optional[JsPackageInfo] = None
    py: Optional[PyPackageInfo] = None
    rs: Optional[RsPackageInfo] = None

    def __post_init__(self):
        for lang in self.languages.values():
            lang.pkg = self

    @property
    def proc_env(self):
        env = dict(
            VERSION=self.version,
            COMPONENT_ROOT=self.path,
            SRC=self.root_dir,
        )

        if self.js:
            env |= self.js.proc_env

        if self.py:
            env |= self.py.proc_env

        return env

    def __hash__(self):
        return hash(str(self.path))

    def __eq__(self, other):
        if isinstance(other, Package):
            return str(self.path) == str(other.path)
        else:
            return NotImplemented

    def resolve_path(self, path):
        return join(self.path, path)

    @classmethod
    def create(cls, config_path, path, manifests, root_dir):
        src_dir = get_source_dir(path)

        config = cls.__load_config(config_path)

        languages = {
            lang.name: cls.__load_lang(lang, path)
            for lang, path in manifests.items()
        }

        lang_configs = iter(languages.values())
        first_config = next(lang_configs)

        version_mismatch = False
        name_mismatch = False
        for lang in lang_configs:
            if lang.version != first_config.version:
                version_mismatch = True

            if lang.canonical_name != first_config.canonical_name:
                name_mismatch = True

        if version_mismatch:
            warn(
                f'Package {config.name} at {path} has '
                + 'mismatched versions.',
                InvalidMetadata,
            )

        if name_mismatch:
            warn(
                f'Package {config.name} at {path}'
                + ' has mismatched names.',
                InvalidMetadata,
            )

        if not is_valid_unscoped_name(config.name):
            warn(
                f'The package at {path} has an invalid name.',
                InvalidMetadata,
            )

        return cls(
            name=config.name,
            path=path,
            version=first_config.version,
            src_dir=src_dir,
            config=config,
            config_path=config_path,
            root_dir=root_dir,
            rel_path=relative_path(path, root_dir),
            languages=languages,
            **languages
        )

    @classmethod
    def __load_config(self, path):
        result = model.structs.package_config.load_file(path)

        return result

    @lang_func(Languages.js)
    def __load_lang(cls, path):
        if path is None:
            return None

        with open(path) as file:
            result = json.load(file)

        return JsPackageInfo(result, path)

    @__load_lang(Languages.py)
    def __load_lang(cls, path):
        if path is None:
            return None

        with open(path) as file:
            text = file.read()

        try:
            result = toml.parse(text)
        except Exception as err:
            raise TomlParseError(f'Toml parse error in {path}') from err
        else:
            return PyPackageInfo(result, path)

    @__load_lang(Languages.rs)
    def __load_lang(cls, path):
        if path is None:
            return None

        with open(path) as file:
            text = file.read()

        try:
            result = toml.parse(text)
        except Exception as err:
            raise TomlParseError(f'Toml parse error in {path}') from err
        else:
            return RsPackageInfo(result, path)

    def __rich_repr__(self):
        yield self.name
        yield 'version', self.version
        yield 'path', self.path


@public
def find_packages(
    search_root: str = None,
    Package: Package = Package,
    iter=False,
    sort=False,
):
    root = find_root(search_root)
    fs = build_tree(root)

    packages_iter = _find_packages(
        '/',
        fs,
        Package,
        root_dir=fspath(root),
    )

    if iter and not sort:
        return packages_iter
    else:
        if sorted:
            packages_iter = sorted(
                packages_iter,
                key=attrgetter('config.name'),
            )

        packages_iter = PackageGroup(packages_iter)

        log.info('Found all packages')

        return packages_iter


def convert_path(root_dir, repo_path):
    repo_path = relpath(repo_path)

    return combine(root_dir, repo_path)


def package_from_dir(
    fs: FS,
    dir: str,
    repo_root: str,
    Package: Package = Package,
):
    lang_manifests = {}

    js_man_path = combine(dir, 'package.json')

    if fs.exists(js_man_path):
        lang_manifests[Languages.js] = convert_path(repo_root, js_man_path)

    py_man_path = combine(dir, 'pyproject.toml')

    if fs.exists(py_man_path):
        lang_manifests[Languages.py] = convert_path(repo_root, py_man_path)

    rs_man_path = combine(dir, 'Cargo.toml')

    if fs.exists(rs_man_path):
        lang_manifests[Languages.rs] = convert_path(repo_root, rs_man_path)

    pkg_config_path = None

    for file in possible_packages_configs:
        possible_path = combine(dir, file)
        if fs.exists(possible_path):
            pkg_config_path = convert_path(repo_root, possible_path)
            break

    if lang_manifests and pkg_config_path:
        return Package.create(
            pkg_config_path,
            convert_path(repo_root, dir),
            lang_manifests,
            repo_root,
        )


def _find_packages(
    search_dir: str,
    fs: FS,
    Package: Package,
    root_dir: str,
):
    if pkg := package_from_dir(fs, search_dir, root_dir, Package):
        yield pkg
    else:
        sub_dirs = (
            combine(search_dir, entry.name)
            for entry in fs.scandir(search_dir, namespaces=['basic'])
            if entry.is_dir
        )

        for dir in sub_dirs:
            yield from _find_packages(dir, fs, Package, root_dir)


@public
def find_nearest(search_root: PathLike, Package=Package) -> Package:
    repo_root = fspath(find_root(search_root))

    search_root = fspath(search_root)

    if not is_dir(search_root):
        search_root = dirname(search_root)

    if not isparent(repo_root, search_root):
        raise FileNotFoundError(
            f'{search_root} is not below {repo_root}',
        )

    rel_search = abspath(relative_path(search_root, repo_root))
    tree = build_tree(repo_root)

    with suppress(DirectoryExists):
        tree.makedirs(rel_search)

    for search_dir in recursepath(rel_search, reverse=True):
        if search_dir == '/':
            break

        if pkg := package_from_dir(tree, search_dir, repo_root, Package):
            return pkg

    raise FileNotFoundError(f'No package found above {search_root}')
