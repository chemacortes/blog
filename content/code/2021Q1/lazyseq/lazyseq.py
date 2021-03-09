"""
Secuencias perezosas creadas a partir de un iterador

- `LazySequence`: secuencia que cachea los elementos obtenidos de un iterador
- `LazySortedSequence`: secuencia perezosa de elementos ordenados

>>> class Squares(LazySortedSequence[int]):
...     def __init__(self):
...         super().__init__(i * i for i in range(0, INFINITE))
>>> s = Squares()
>>> 10000 in s
True
>>> s[:100]
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100, 121, 144, 169, 196, 225, 256, 289, \
324, 361, 400, 441, 484, 529, 576, 625, 676, 729, 784, 841, 900, 961, 1024, \
1089, 1156, 1225, 1296, 1369, 1444, 1521, 1600, 1681, 1764, 1849, 1936, 2025, \
2116, 2209, 2304, 2401, 2500, 2601, 2704, 2809, 2916, 3025, 3136, 3249, 3364, \
3481, 3600, 3721, 3844, 3969, 4096, 4225, 4356, 4489, 4624, 4761, 4900, 5041, \
5184, 5329, 5476, 5625, 5776, 5929, 6084, 6241, 6400, 6561, 6724, 6889, 7056, \
7225, 7396, 7569, 7744, 7921, 8100, 8281, 8464, 8649, 8836, 9025, 9216, 9409, \
9604, 9801]
"""


import sys
from bisect import bisect_left
from collections.abc import Iterator
from functools import singledispatchmethod
from itertools import islice
from typing import Optional, TypeVar

INFINITE = sys.maxsize  # una mala aproximación de infinito

# Generic Types
T = TypeVar("T", covariant=True)
Ord = TypeVar("Ord", bound=int, covariant=True)


class LazySequence(Iterator[T]):
    """
    Secuencia perezosa creada a partir de un iterador
    """

    def __init__(self, iterator: Iterator[T]):
        self._cache: list[T] = []
        self.iterator = iterator

    @property
    def last(self) -> Optional[T]:
        return self._cache[-1] if self.size > 0 else None

    @property
    def size(self) -> int:
        return len(self._cache)

    def __next__(self) -> T:
        x = next(self.iterator)
        self._cache.append(x)
        return x

    def __iter__(self) -> Iterator[T]:
        yield from self._cache
        yield from (self[i] for i in range(len(self._cache), INFINITE))

    def islice(self, start, stop=-1, step=1) -> Iterator[T]:
        if stop == -1:
            start, stop = 0, start
        if stop is None:
            stop = INFINITE
        yield from (self[i] for i in range(start, stop, step))

    @singledispatchmethod
    def __getitem__(self, idx):
        return NotImplemented

    @__getitem__.register
    def __getitem_int__(self, idx: int) -> T:
        if idx < 0:
            raise OverflowError
        elif idx >= self.size:
            self._cache.extend(islice(self.iterator, idx - self.size + 1))

        return self._cache[idx]

    @__getitem__.register
    def __getitem_slice__(self, sl: slice) -> list[T]:
        rng = range(INFINITE)[sl]
        return [self[i] for i in rng]


class LazySortedSequence(LazySequence[Ord]):
    """
    Secuencia perezosa ordenada creada a partir de un iterador
    """

    def insertpos(self, x: int) -> int:
        """
        Posición donde insertar un elemento para mantener la lista ordenada
        Obtiene los elementos necesarios hasta llegar a la posición
        """
        if self.size > 0 and x <= self.last:
            idx = bisect_left(self._cache, x)
        else:
            while x > next(self):
                pass
            idx = self.size - 1

        return idx

    def __contains__(self, x: int) -> bool:
        idx = self.insertpos(x)
        return x == self._cache[idx]

    def index(self, x: int) -> int:
        idx = self.insertpos(x)
        if x == self._cache[idx]:
            return idx
        raise ValueError(f"{x} is not in {self.__class__.__name__}")
