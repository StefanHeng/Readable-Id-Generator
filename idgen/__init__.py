import numpy as np

from util import *


class IdGen:
    """
    Randomly generates a set of human-readable words or word-pairs, in particular

    Opinionated - Words of shorter length are more likely to be sampled
    """
    def __init__(self):
        self.adjs = load_corpus('adjectives.txt')
        self.nouns = load_corpus('nouns.txt')
        self.vocab = self.adjs + self.nouns
        self.n_adj, self.n_noun = len(self.adjs), len(self.nouns)
        self.dec_adj = {i: wd for i, wd in enumerate(self.adjs)}
        self.dec_noun = {i: wd for i, wd in enumerate(self.nouns)}
        # length A
        lens_adj = np.fromiter((len(wd) for wd in self.adjs), dtype=int, count=len(self.adjs)).reshape(-1, 1)
        lens_noun = np.fromiter((len(wd) for wd in self.nouns), dtype=int, count=len(self.nouns))  # Length N
        lens_pair = (lens_adj + lens_noun).flatten()
        self.lens = np.concatenate((lens_noun, (lens_adj + lens_noun).flatten()))  # Lengths of A + A * N
        self.n_opns = self.lens.size  # Total possible words

        ic(self.adjs[:5], self.nouns[:5])
        ic(self.lens.shape)
        idx_adj, idx_noun = 1511, 2023
        ic(lens_pair.shape)
        ic(lens_pair.shape, lens_pair[idx_adj * len(self.nouns) + idx_noun], self.adjs[idx_adj], self.nouns[idx_noun])
        idx_ = idx_adj * len(self.nouns) + idx_noun
        ic(idx_, self.idx2wd(idx_))

        self.probs = 1 / np.square(self.lens)  # Penalize by phrase length, quadratically
        self.probs /= self.probs.sum()  # Normalize
        ic(self.probs[:20], self.probs[-20:], self.probs.shape)

    def idx2wd(self, idx: int) -> str:
        if idx < self.n_noun:
            return self.dec_noun[idx]
        else:
            idx -= self.n_noun
            idx_adj, idx_noun = idx // self.n_noun, idx % self.n_noun
            return f'{self.dec_adj[idx_adj]}-{self.dec_noun[idx_noun]}'

    def __call__(self, sz: int = 2**12, sort=True) -> Iterable[str]:
        """
        :param sz: Vocabulary size
        :param sort: If true, words are ordered in ascending order of length
        """
        if sz > self.n_opns:
            raise ValueError(f'Vocabulary size too large: got {sz}, expect <={self.n_opns}'
                             f' - Consider increasing corpus size')
        idxs = np.random.choice(self.n_opns, size=sz, replace=False, p=self.probs)
        lens = self.lens[idxs]
        if sort:
            idxs = idxs[np.argsort(lens)]
        for i in idxs:
            yield self.idx2wd(i)
            # ic(idxs_, 'sort')
        # ic(idxs)


if __name__ == '__main__':
    from icecream import ic

    np.random.seed(77)

    ig = IdGen()
    vocab = list(ig())
    ic(vocab[:20], vocab[-20:])
