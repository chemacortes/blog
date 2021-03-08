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


if __name__ == "__main__":

    class Squares(LazySortedSequence[int]):
        def __init__(self):
            super().__init__(i * i for i in range(0, INFINITE))

    s = Squares()

    100000 in s
    s[:100]
