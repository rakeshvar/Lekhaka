from collections import namedtuple

import numpy as np
import pickle
import gzip
from pathlib import  Path

print("*"*88, "\nLoading the uni and bigram counts")
this_dir= Path(__file__).parent                           # .reslove()

akshara_path = this_dir / "data" / "akshara_bigram.pkl.gz"
char_path = this_dir / "data" / "char_gram.pkl.gz"


def load_dicts(filename):
    with gzip.open(filename, 'rb') as f:
        data = pickle.load(f)
        return data['uni'], data['bi'], data['tri']

def norm(m, fn=None):
    if m is None:
        return  None
    if fn == np.log2:
        m += 1
    if fn is not None:
        m = fn(m)
    return m/m.sum(axis=-1, keepdims=True)

class Sampler:
    def __init__(self, filename, level):
        unid, bi_d, trid = load_dicts(filename)
        self.n = len(unid)

        self.itos = itos = sorted(list(unid.keys()))
        self.stoi = {s:i for i, s in enumerate(itos)}

        u = np.array([unid[s] for s in itos])
        b = np.array([[bi_d[s].get(t, 0) for t in itos] for s in itos])

        t = np.array([[[
            trid[s][t].get(u, 0) if t in trid[s] else 0
            for u in itos] for t in itos] for s in itos]) if level == 3 else None

        print("Loaded ", filename)
        print(f"Bi-gram  size: {b.size:>12,}")
        print(f"Tri-gram size: {0 if t is None else t.size:>12,}")

        Grams = namedtuple("Grams", ["uni", "bi", "tri"])
        self.grams = {
            "orig" : Grams(uni=norm(u), bi=norm(b), tri=norm(t)),
            "sqrt" : Grams(uni=norm(u, np.sqrt), bi=norm(b, np.sqrt), tri=norm(t, np.sqrt)),
            "log2" : Grams(uni=norm(u, np.log2), bi=norm(b, np.log2), tri=norm(t, np.log2))
        }

    def get_next(self, scaling:str, ti:int, si=None):
        g = self.grams[scaling]
        if si is None or g.tri is None or np.isnan(g.tri[si, ti, 0]):
            probs = g.bi[ti]
        else:
            probs = g.tri[si, ti]
        try:
            return np.random.choice(self.n, p=probs)
        except ValueError:
            print(f"{si} {ti} {probs}")

    def get_word(self, length, scaling):
        si, ti = None, self.stoi[' ']
        sample_text = []

        for l in range(length):
            si, ti = ti, self.get_next(scaling, ti, si)
            t = ' ' if self.itos[ti] in "\n\x1e" else self.itos[ti]
            sample_text.append(t)

        return ''.join(sample_text)


char_tri = Sampler(char_path, 3)
akshara_bi = Sampler(akshara_path, 2)

count = 0
def get_word(length):
    global count
    count += 1
    if not count % 2:
        return char_tri.get_word(3*length//2, "orig")
    else:
        return akshara_bi.get_word(length, "sqrt")


if __name__ == "__main__":
    L = 60
    N = 100
    for scale in ("orig", "sqrt", "log2"):
        print("\n### char # ", scale)
        for i in range(N):
            print(char_tri.get_word(3*L//2, scale))
        print("\n*** aksh *", scale)
        for i in range(N):
            print(akshara_bi.get_word(L, scale))
