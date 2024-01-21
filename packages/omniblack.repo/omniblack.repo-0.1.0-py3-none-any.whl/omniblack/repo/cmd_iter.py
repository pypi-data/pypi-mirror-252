from itertools import takewhile, chain


def null_seperated(stream):
    stream = chain.from_iterable(stream)

    while item := ''.join(takewhile(lambda c: c != '\0', stream)):
        yield item
