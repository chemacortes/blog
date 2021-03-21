# %% [markdown]
"""
Secuencia perezosa de números primos
====================================

## Doctests

```python
>>> isprime(2 ** 31 - 1)
True
>>> primes[90000]
1159531
>>> primes.index(1159531)
90000
>>> primes.size
90001
>>> primes.last
1159531

```
"""

# %%

from collections.abc import Iterator
from itertools import islice
from math import isqrt
from typing import final

from lazyseq import LazySortedSequence

Prime = int


@final
class Primes(LazySortedSequence[Prime]):
    def __init__(self):
        super().__init__(self.__genprimes())
        self._cache.extend([2, 3])

    def __genprimes(self) -> Iterator[Prime]:
        _primes = self._cache
        start = 5
        top = 1
        while True:
            stop = _primes[top] ** 2
            for n in range(start, stop, 2):
                for p in islice(_primes, 1, top):
                    if n % p == 0:
                        break
                else:
                    yield n

            start = stop + 2
            top += 1

    def __contains__(self, n: int) -> bool:

        if n <= self.last:
            return super().__contains__(n)

        root = isqrt(n)
        _primes = self._cache

        top = self.size if root > self.last else self.insertpos(root)

        if any(n % prime == 0 for prime in islice(_primes, 1, top)):
            return False

        # "one-shot" check
        if any(n % i == 0 for i in range(self.last + 2, root + 1, 2)):
            return False

        return True


primes = Primes()
isprime = primes.__contains__
