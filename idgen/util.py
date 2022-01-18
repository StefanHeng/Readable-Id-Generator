import os
import itertools
from collections.abc import Iterable
from typing import TypeVar, Callable
import concurrent.futures


def load_corpus(fnm, path='corpus') -> list[str]:
    with open(os.path.join(path, fnm)) as f:
        return [wd.strip() for wd in f.readlines()]


T = TypeVar('T')
K = TypeVar('K')


def join_its(*its: Iterable[Iterable[T]]) -> Iterable[T]:
    out = itertools.chain()
    for it in its:
        out = itertools.chain(out, it)
    return out


def conc_map(fn: Callable[[T], K], it: Iterable[T]) -> Iterable[K]:
    """
    Wrapper for `concurrent.futures.map`

    :param fn: A function
    :param it: A list of elements
    :return: Iterator of `lst` elements mapped by `fn` with concurrency
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        return executor.map(fn, it)
