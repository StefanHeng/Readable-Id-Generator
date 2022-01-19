from typing import Iterator, Callable

import numpy as np
from numpy.random import default_rng

from readableidgen.util import *


class Mappings:
    """
    Functions that maps length to weights of being drawn in `IdGen`

    Always penalize longer sequences
    """
    @staticmethod
    def LARGE(lens):
        """
        Ratio between shortest & longest sequence ~1e17
        """
        return np.exp(lens.mean() - lens)


class IdGen:
    """
    Randomly generates a set of human-readable words or word-pairs, in particular

    Opinionated - Words of shorter length are more likely to be sampled
    """
    def __init__(
            self,
            adjs: list[str] = None, nouns: list[str] = None,
            fn: Callable[[np.ndarray], np.ndarray] = lambda lens: 1 / np.square(lens),  # Penalize quadratically
            verbose=False,
            rng=None
    ):
        """
        :param adjs: Corpus for adjectives
        :param nouns: Corpus for nouns
        :param fn: Penalization function, mapping the length of each phrase to its weight
        :param verbose: If True, each vocabulary generation call logged to console
        :param rng: Numpy random number generator

        .. note:: If not given, internal dictionary is loaded
        """
        self.adjs = load_corpus('adjectives.txt') if adjs is None else adjs
        self.nouns = load_corpus('nouns.txt') if nouns is None else nouns
        self.n_adj, self.n_noun = len(self.adjs), len(self.nouns)
        self.dec_adj = {i: wd for i, wd in enumerate(self.adjs)}
        self.dec_noun = {i: wd for i, wd in enumerate(self.nouns)}
        # length A
        lens_adj = np.fromiter((len(wd) for wd in self.adjs), dtype=int, count=len(self.adjs)).reshape(-1, 1)
        lens_noun = np.fromiter((len(wd) for wd in self.nouns), dtype=int, count=len(self.nouns))  # Length N
        self.lens = np.concatenate((lens_noun, (lens_adj + lens_noun).flatten()))  # Length of A + A * N
        self.n_opns = self.lens.size  # Total possible words

        self.probs = fn(self.lens).astype(float)
        self.probs /= self.probs.sum()  # Normalize

        self.verbose = verbose
        if rng is None:
            self.rng = default_rng()
        else:
            self.rng = rng

    def idx2wd(self, idx: int) -> str:
        if idx < self.n_noun:
            return self.dec_noun[idx]
        else:
            idx -= self.n_noun
            idx_adj, idx_noun = idx // self.n_noun, idx % self.n_noun
            return f'{self.dec_adj[idx_adj]}-{self.dec_noun[idx_noun]}'

    def __call__(self, sz: int = 2**12, sort=True) -> Iterator[str]:
        """
        :param sz: Vocabulary size
        :param sort: If true, words are ordered in ascending order of length
        """
        if self.verbose:
            log(f'Creating random word dictionary of size {logi(sz)}, on corpus of {logi(self.n_opns)} options... ')
        if sz > self.n_opns:
            raise ValueError(f'Vocabulary size too large: got {sz}, expect <={self.n_opns}'
                             f' - Consider increasing corpus size')
        idxs = self.rng.choice(self.n_opns, size=sz, replace=False, p=self.probs)
        lens = self.lens[idxs]
        if sort:
            idxs = idxs[np.argsort(lens)]
        for i in idxs:
            yield self.idx2wd(i)


if __name__ == '__main__':
    from icecream import ic

    # np.random.seed(77)
    rng = default_rng(77)
    n = 20

    def sanity_check():
        ig = IdGen(verbose=True, rng=rng)
        vocab = list(ig())
        assert len(vocab) == len(set(vocab))
        ic(type(ig()))
        ic(vocab[:n], vocab[-n:], np.array([len(wd) for wd in vocab]).mean())
    sanity_check()

    def explore_fn():
        # ig_ = IdGen(fn=lambda lens: 1 / (lens**3))
        # ig_ = IdGen(fn=lambda lens: (lens.max()+1 - lens) ** 8)
        ig_ = IdGen(fn=Mappings.LARGE)
        vocab_ = list(ig_())
        ic(vocab_[:n], vocab_[-n:], np.array([len(wd) for wd in vocab_]).mean())
    explore_fn()
