import sys
from bisect import bisect, bisect_left
from collections.abc import Generator, Iterable, Iterator
from functools import singledispatchmethod
from itertools import islice
from math import isqrt

INFINITE = sys.maxsize  # una mala aproximación de infinito
Prime = int  # un alias para los primos


def nth(it: Iterable, n: int):
    """Obtener el elemento en la posición 'n' de un iterable"""
    return next(islice(it, n, None))


# ----------------------------------------
# Versiones 'bisect' para listas ordenadas
#


def bs_index(lst: list, x) -> int:
    idx = bisect_left(lst, x)
    if idx < len(lst) and lst[idx] == x:
        return idx
    return -1


def bs_contains(lst: list, x) -> bool:
    idx = bisect_left(lst, x)
    return idx < len(lst) and lst[idx] == x


def bs_range(lst: list[int], x: int) -> Iterator[int]:
    idx = bisect(lst, x)
    return islice(lst, 1, idx)


# ----------------------------------------


class Primes:
    """
    Collection of primes numbers
    """

    def __init__(self):
        self._primes: list[Prime] = [2, 3]

    @property
    def last(self) -> Prime:
        return self._primes[-1]

    @property
    def size(self) -> int:
        return len(self._primes)

    def __len__(self) -> int:
        return INFINITE

    def __contains__(self, n: int) -> bool:
        # if n in self._primes: return True
        if n <= self.last:
            return bs_contains(self._primes, n)

        root = isqrt(n)

        # stop = bisect(self._primes, root)
        # if any(n % prime == 0 for prime in islice(self._primes, 1, stop)):
        #     return False
        if any(n % prime == 0 for prime in bs_range(self._primes, root)):
            return False

        # "one-shot" check
        if any(n % i == 0 for i in range(self.last + 2, root + 1, 2)):
            return False

        return True

    def genprimes(self) -> Generator[Prime, None, None]:
        """Generador de los 'siguientes' números primos"""

        start = self.last + 2
        top = bisect(self._primes, isqrt(start))
        while True:
            stop = self._primes[top] ** 2
            for n in range(start, stop, 2):
                for p in islice(self._primes, 1, top):
                    if n % p == 0:
                        break
                else:
                    self._primes.append(n)
                    yield n

            start = stop + 2
            top += 1

    @singledispatchmethod
    def __getitem__(self, idx):
        return NotImplemented

    @__getitem__.register
    def __getitem_int__(self, idx: int) -> Prime:
        if idx < 0:
            raise OverflowError

        return (
            self._primes[idx]
            if idx < self.size
            else nth(self.genprimes(), idx - self.size)
        )

    @__getitem__.register
    def __getitem_slice__(self, sl: slice) -> list[Prime]:
        rng = range(INFINITE)[sl]
        return [self[i] for i in rng]

    def index(self, n: Prime) -> int:

        if n > self.last:
            gen = self.genprimes()
            while n > next(gen):
                pass

        idx = bs_index(self._primes, n)
        if idx != -1:
            return idx
        raise ValueError(f"{n} is not a prime number")

    def count(self, n: int) -> int:
        return 1 if n in self else 0

    def __iter__(self) -> Iterator[Prime]:
        yield from (self[i] for i in range(0, INFINITE))


primes = Primes()
isprime = primes.__contains__
