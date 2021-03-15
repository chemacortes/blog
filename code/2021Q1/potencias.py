"""
Potencias de primos con exponentes potencias de dos
===================================================

Se llaman **potencias de Fermi-Dirac** a los números de la forma p^(2^k), donde
p es un número primo y k es un número natural.

Definir la sucesión

   potencias :: [Integer]

cuyos términos sean las potencias de Fermi-Dirac ordenadas de menor a mayor.
Por ejemplo,

   take 14 potencias    ==  [2,3,4,5,7,9,11,13,16,17,19,23,25,29]
   potencias !! 60      ==  241
   potencias !! (10^6)  ==  15476303
"""

# %%

from collections.abc import Iterator
from itertools import count, islice
from typing import TypeVar

from primes import primes

# Se vincula al tipo int, ya que no existe protocolo Ord o Sortable
T = TypeVar("T", bound=int)

SortedIterator = Iterator


def join(s1: SortedIterator[T], s2: SortedIterator[T]) -> SortedIterator[T]:
    x = next(s1)
    y = next(s2)
    while True:
        if x <= y:
            yield x
            x = next(s1)
        else:
            yield y
            y = next(s2)


def flat(it: Iterator[SortedIterator[T]]) -> SortedIterator[T]:
    s1 = next(it)
    yield next(s1)
    yield from join(s1, flat(it))


def potencias_gen(k: int) -> SortedIterator[int]:
    yield from (p ** 2 ** k for p in primes)


def potencias() -> SortedIterator[int]:
    yield from flat(potencias_gen(k) for k in count())


if __name__ == "__main__":

    def nth(it, n):
        return next(islice(it, n, None))

    # take 14 potencias    ==  [2,3,4,5,7,9,11,13,16,17,19,23,25,29]
    print(list(islice(potencias(), 14)))

    # potencias !! 60      ==  241
    print(nth(potencias(), 60))

    # potencias !! (10^6)  ==  15476303
    print(nth(potencias(), 10 ** 6))

    # límites
    print(
        f"Obtenidos {primes.size} números primos, siendo {primes.last} el mayor"
    )
