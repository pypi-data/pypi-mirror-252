from requests import Session
from re import compile
from rich import pretty


pretty.install()

code_point = '[0-9A-F]{4}'

line_regex = compile(
    rf'^(?:(?P<code_point>{code_point})'
    + rf'|(?:(?P<start>{code_point})..(?P<end>{code_point}))) +; XID_Start',
)

url = 'https://www.unicode.org/Public/14.0.0/ucd/DerivedCoreProperties.txt'


class ListView:
    __slots__ = (
        '__start',
        '__stop',
        '__list',
    )

    def __init__(self, start, stop, list):
        self.__start = start
        self.__stop = stop
        self.__list = list

    def __len__(self):
        return self.__stop - self.__start

    def __getitem__(self, index):
        if isinstance(index, int):
            if index < 0:
                index = len(self) + index

            adjusted = index + self.__start
            if adjusted >= self.__stop:
                raise IndexError('list index out of range', index)

            return self.__list[adjusted]
        elif isinstance(index, slice):
            assert index.step is None
            (new_start, new_stop, _) = index.indices(len(self))
            new_start += self.__start
            new_stop += self.__start

            return type(self)(new_start, new_stop, self.__list)

    def __iter__(self):
        for index in range(self.__start, self.__stop):
            yield self.__list[index]

    def __reversed__(self):
        for index in reversed(range(self.__start, self.__stop)):
            yield self.__list[index]

    def __repr__(self):
        cls_name = type(self).__name__
        item_reprs = (
            repr(item)
            for item in self
        )
        return f'{cls_name}[{", ".join(item_reprs)}]'

    def __rich_repr__(self):
        our_slice = self.__list[self.__start:self.__stop]
        yield our_slice

    __rich_repr__.angular = True

    def __bool__(self):
        return bool(len(self))


def binary_search(array, target):
    view = ListView(0, len(array), array)

    while view:
        if view[0] > target or view[-1] < target:
            return None

        mid_point = (len(view) - 1) // 2

        mid_item = view[mid_point]

        if mid_item == target:
            return mid_item
        elif mid_item < target:
            view = view[mid_point + 1:]
        elif mid_item > target:
            view = view[:mid_point]

    return None


class UnicodeRange:
    __slots__ = (
        'start',
        'end',
    )

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def __gt__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        return self.start > other

    def __lt__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        return self.end < other

    def __eq__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        return other in self

    def __contains__(self, other):
        if not isinstance(other, int):
            return NotImplemented

        return self.start <= other and self.end >= other

    def __rich_repr__(self):
        yield self.start
        yield self.end

    def __bool__(self):
        return True


def process_line(match, ranges):
    if match['start']:
        start = int(match['start'], 16)
        end = int(match['end'], 16)

        ranges.append(UnicodeRange(start, end))
    else:
        ranges.append(int(match['code_point'], 16))


with Session() as s:
    with s.get(url, stream=True) as resp:
        line_iter = resp.iter_lines(decode_unicode=True)

        ranges = []

        for line in line_iter:
            if match := line_regex.match(line):
                process_line(match, ranges)
                break

        for line in line_iter:
            if match := line_regex.match(line):
                process_line(match, ranges)
            else:
                break


def is_xid_char(char):
    return bool(binary_search(ranges, ord(char)))


def ensure_id_start(string):
    if is_xid_char(string[0]):
        return string
    else:
        return '_' + string
