from typing import Protocol, runtime_checkable
from collections.abc import Mapping
from warnings import warn
from os.path import dirname

from rich.repr import auto
from public import public

from .display import error
from .metadata_warning import InvalidMetadata
from .names import canonicalize_name
from .version import Version
from .languages import Languages


@public
@runtime_checkable
@auto
class PackageInfo(Protocol):
    name: str
    version: Version
    path: str
    canonical_name: str
    manifest: Mapping
    language: Languages
    private: bool = False

    @property
    def proc_env(self):
        return {
            f'{self.language.upper()}_NAME': self.name,
            f'{self.language.upper()}_MANIFEST': self.path,
        }

    @property
    def __id_keys(self):
        return (
            self.version,
            self.canonical_name,
            self.language,
            self.path,
        )

    def __eq__(self, other):
        if not isinstance(other, PackageInfo):
            return NotImplemented

        return self.__id_keys == other.__id_keys

    def __hash__(self):
        return hash(self.__id_keys)

    def __rich_repr__(self):
        yield self.name
        yield 'path', self.path
        yield 'version', self.version

        if self.canonical_name != self.name:
            yield 'canonical_name', self.canonical_name

        yield 'manifest', self.manifest


class JsPackageInfo(PackageInfo):
    language = Languages.js

    def __init__(self, pkg_json: Mapping, path: str):
        self.manifest = pkg_json
        self.path = path
        self.version = Version(pkg_json['version'])
        self.name = pkg_json['name']
        self.private = pkg_json.get('private', False)

        try:
            self.canonical_name = canonicalize_name(self.name, self.language)
        except ValueError:
            error.print_exception()
            self.canonical_name = self.name
            pkg_path = dirname(path)
            warn(
                f'Package at {pkg_path} does not have a '
                + 'valid name in package.json.',
                category=InvalidMetadata,
            )


private_clasifier = 'Private :: Do Not Upload'


class PyPackageInfo(PackageInfo):
    language = Languages.py

    def __init__(self, pyproject, path: str):
        self.manifest = pyproject
        project = pyproject['project']
        self.version = Version(project['version'])
        self.name = project['name']
        self.path = path
        self.private = private_clasifier in project.get('classifiers', [])

        try:
            self.canonical_name = canonicalize_name(self.name, self.language)
        except ValueError:
            error.print_exception()
            self.canonical_name = self.name
            pkg_path = dirname(path)
            warn(
                f'Package at {pkg_path} does not have a '
                + 'valid name in pyproject.toml.',
                category=InvalidMetadata,
            )

    @property
    def is_extenstion(self):
        return (
            self.pkg.rs
            and 'pyo3' in self.pkg.rs.manifest.get('dependencies', {})
        )


class RsPackageInfo(PackageInfo):
    language = Languages.rs

    def __init__(self, cargo_toml, path):
        self.manifest = cargo_toml
        pkg = cargo_toml['package']

        self.version = Version(pkg['version'])
        self.name = pkg['name']
        self.path = path
        self.private = not pkg.get('publish', True)

        try:
            self.canonical_name = canonicalize_name(self.name, self.language)
        except ValueError:
            error.print_exception()
            self.canonical_name = self.name
            pkg_path = dirname(path)
            warn(
                f'Package at {pkg_path} does not have a '
                + 'valid nam in Cargo.toml',
                category=InvalidMetadata,
            )
