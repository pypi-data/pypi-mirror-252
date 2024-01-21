from logging import getLogger
from os import environ, getcwd
from os.path import realpath
from subprocess import CalledProcessError
from public import public
from subprocess import run


log = getLogger(__name__)

check_commands = (
    ('git', 'rev-parse', '--show-toplevel'),

    # These are untested
    ('hg', 'root'),
    ('svn', 'info', '--show-item', 'wc-root'),
)


@public
def find_root(search_path: str = None):
    if 'SRC' in environ:
        return environ['SRC']
    elif 'GIT_WORK_TREE' in environ:
        return environ['GIT_WORK_TREE']
    else:
        if search_path is None:
            search_path = getcwd()
        else:
            search_path = realpath(search_path)

        for cmd in check_commands:
            try:
                result = run(
                    cmd,
                    cwd=search_path,
                    check=True,
                    capture_output=True,
                )
                path_str = result.stdout.decode().strip()

                return path_str
            except CalledProcessError:
                pass

        return None
