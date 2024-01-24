import sh
from sh import CommandNotFound, ErrorReturnCode_255, ErrorReturnCode_128

from .find_root import find_root
from .cmd_iter import null_seperated

check_commands = (
    ('git', 'ls-files', '-z'),

    # These are untested
    ('hg', 'files', '--print0', '--pager', 'never'),
    # Could not find a reasonable command for svn to get all files
    # So they don't get support
)


def list_files(search_root=None):
    if search_root is None:
        search_root = find_root()

    for cmd_str, *args in check_commands:
        try:
            cmd = getattr(sh, cmd_str)
            running = cmd(
                *args,
                _iter=True,
                _out_bufsize=8 * 4,
                _bg_exc=False,
                _cwd=search_root,
            )
            yield from null_seperated(running)
        except (CommandNotFound, ErrorReturnCode_255, ErrorReturnCode_128):
            continue
        else:
            return
