# %% [markdown]
"""
Potencias de primos con exponentes potencias de dos
===================================================

Se llaman **potencias de Fermi-Dirac** a los números de la forma $p^{2^k}$,
donde p es un número primo y k es un número natural.

Definir la sucesión

```haskell
potencias :: [Integer]
```

cuyos términos sean las potencias de Fermi-Dirac ordenadas de menor a mayor. Por
ejemplo,

```haskell
take 14 potencias    ==  [2,3,4,5,7,9,11,13,16,17,19,23,25,29]
potencias !! 60      ==  241
potencias !! (10^6)  ==  15476303
```

## Doctests:

```python
>>> potencias[:14]
[2, 3, 4, 5, 7, 9, 11, 13, 16, 17, 19, 23, 25, 29]
>>> potencias[60]
241
>>> potencias[10 ** 6]
15476303
>>> potencias.index(15476303)
1000000
>>> potencias.index(15476304)
Traceback (most recent call last):
ValueError: 15476304 is not in LazySortedSequence
>>> # límites
>>> print(f"Obtenidos {primes.size} números primos, {primes.last} el mayor")
Obtenidos 999433 números primos, 15476333 el mayor

```
"""

# %%

from collections.abc import Iterator
from itertools import count
from typing import TypeVar

from lazyseq import LazySortedSequence
from primes import primes

# Se vincula al tipo int, ya que no existe protocolo Ordered o Sortable
Ord = TypeVar("Ord", bound=int)

SortedIterator = Iterator[Ord]


def join(s1: SortedIterator, s2: SortedIterator) -> SortedIterator:
    x = next(s1)
    y = next(s2)
    while True:
        if x <= y:
            yield x
            x = next(s1)
        else:
            yield y
            y = next(s2)


def flat(it: Iterator[SortedIterator]) -> SortedIterator:
    s1 = next(it)
    yield next(s1)
    yield from join(s1, flat(it))


def mkiter(k):
    yield from (p ** 2 ** k for p in primes)


potencias = LazySortedSequence(flat(mkiter(k) for k in count()))
