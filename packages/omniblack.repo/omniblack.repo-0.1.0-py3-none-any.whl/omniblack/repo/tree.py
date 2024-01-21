from os.path import dirname, join
from contextlib import suppress
from fs.memoryfs import MemoryFS
from fs.errors import DirectoryExists
from .list_all_files import list_files
from .find_root import find_root


def build_tree(root=None):
    fs = MemoryFS()
    if root is None:
        root = find_root()

    for file in list_files(root):
        file = join('/', file)
        with suppress(DirectoryExists):
            fs.makedirs(dirname(file))

        fs.touch(file)

    return fs
