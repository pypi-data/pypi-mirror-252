import re
from itertools import repeat
from typing import NamedTuple

from packaging.version import Version as _Version
from packaging.utils import canonicalize_version as _canonicalize_version

from public import public


named_release_segs = {
    'major': 0,
    'minor': 1,
    'micro': 2,
    'patch': 2,
}

bumpable_segments = {
    'epoch',
    'post',
    'dev',
}


def canonicalize_version(ver):
    canon_ver = _canonicalize_version(ver)
    return Version(canon_ver)


def no_sep(segs):
    return ''.join(
        str(seg)
        for seg in segs
    )


@public
class Version(_Version):
    def bump(self, segment='patch'):
        if segment in named_release_segs:
            index = named_release_segs[segment]
            release_vals = list(self.release)
            items_needed = max(0, (index + 1) - len(release_vals))
            release_vals.extend(repeat(0, items_needed))
            release_vals[index] += 1

            release_vals[index+1:] = repeat(0, len(release_vals) - (index + 1))

            segment = 'release'
            value = release_vals
        elif segment in bumpable_segments:
            value = getattr(self, segment) + 1
        else:
            raise TypeError(f'"{segment}" is not a bumpable segments.')

        ver = self._version._replace(**{segment: value})

        parts = []

        if ver.epoch != 0:
            parts.append(f'{ver.epoch}!')

        if ver.release:
            parts.append('.'.join(
                str(p)
                for p in ver.release
            ))

        if ver.pre is not None:
            parts.append(no_sep(ver.pre))

        if ver.post is not None:
            parts.append(f'.post{ver.post[1]}')

        if ver.dev is not None:
            parts.append(f'.dev{ver.dev[1]}')

        if ver.local is not None:
            parts.append(f'+{ver.local}')

        return Version(no_sep(parts))

    @classmethod
    def to_yaml(cls, representer, node):
        return representer.represent_str(str(node))
