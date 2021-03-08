---
Title: Formalización de la Secuencia Perezosa - Evaluación perezosa en python - Parte 5
Date: 2021-03-07 23:57:55
Modified: 2021-03-08 01:53:59
Category: Python
Tags: lazy-eval, sequence, primes
Slug: evaluacion-perezosa-en-python-parte-5
Authors: Chema Cortés
Summary: Refactorización del código creado hasta ahora para formalizar las clases `LazySequence` y `LazySortedSequence` para uso general.
Lang: es
Translation: false
Status:
---

## Refactorización

Hasta ahora hemos visto cómo crear una _secuencia perezosa_ que va guardando en
una caché los resultado de una operación (proceso de _memoización_). Así mismo,
hemos visto con la secuencia de números primos que podemos optimizar algunas
búsquedas si la secuencia es una _secuencia ordenada_. Vamos a intentar
formalizar todo esto con las clases `LazySequence` y `LazySortedSequence`.

Descargas del código refactorizado:

- [genericrange.py][]
- [lazyseq.py][]
- [primes.py][]

### LazySequence

La clase `LazySequence` creará una _secuencia perezosa_ a partir de un iterador.
A medida que obtenga elementos del iterador, los irá almacenando en una caché:

```python
T = TypeVar("T", covariant=True)

class LazySequence(Iterator[T]):
    def __init__(self, iterator: Iterator[T]):
        self._cache: list[T] = []
        self.iterator = iterator

    def __next__(self) -> T:
        x = next(self.iterator)
        self._cache.append(x)
        return x
```

Cada vez que se calcule un nuevo elemento a través de `next()`, éste se añadirá
a la caché.

Para que funcione como secuencia, se implementan los métodos `__getitem__`:

```python
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
```

Y añadimos el método `__iter__` para que cumpla con el protocolo _iterador_:

```python
    def __iter__(self) -> Iterator[T]:
        yield from self._cache
        yield from (self[i] for i in range(len(self._cache), INFINITE))
```

### LazySortedSequence

Derivando de `LazySequence`, se crea la clase `LazySortedSequence` para cuando
el iterador produzca una secuencia ordenada. Tal como hemos visto, cuando la
secuencia está ordenada podemos realizar búsquedas por _bisecciones_ que resulta
bastante eficiente.

La operación principal será el método `insertpos()` que nos indica la posición
en la que se insertaría un elemento en la secuencia, siempre manteniendo el
orden. Si no son suficientes con los elementos de la caché, se extraerán más mediante `next()`, lo que irá añadiéndose a la caché:

```python
Ord = TypeVar("Ord", bound=int, covariant=True)

class LazySortedSequence(LazySequence[Ord]):
    def insertpos(self, x: int) -> int:
        if self.size > 0 and x <= self.last:
            idx = bisect_left(self._cache, x)
        else:
            while x > next(self):
                pass
            idx = self.size - 1

        return idx
```

Con el método `insertpos()` ya podemos definir los métodos `__contains__()` e `index()` típicos de la secuencias:

```python
    def __contains__(self, x: int) -> bool:
        idx = self.insertpos(x)
        return x == self._cache[idx]

    def index(self, x: int) -> int:
        idx = self.insertpos(x)
        if x == self._cache[idx]:
            return idx
        raise ValueError(f"{x} is not in {self.__class__.__name__}")
```

No existe un protocolo para elementos _ordenables_ (`Sortable` u `Ordered`).
Para ordenar elementos se usan los métodos de comparación `__eq__`, `__ne__`,
`__lt__`, `__le__`, `__gt__` y `__ge__`. Pero se suele considerar estos métodos
redundantes ya que basta con definir sólo dos (eg: `__eq__` y `__lt__`) para
establecer una ordenación.

Como no hay una forma mejor, se ha enlazado el tipo genérico `Ord` con `int`
para que el chequeador de tipos no se queje en la comparaciónes, aunque no tiene
porqué limitarse a los números enteros.

### Números primos

Como caso práctico, veamos cómo se puede redefinir la clase `Primes`:

```python
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
```

En la implementación que teníamos de la clase `Primes`, el método
`__contains__()` estaba optimizado para limitarse a comprobar la pertencia de un
número, sin añadir más elementos a la caché. Vamos a recuperar esta
codificación:

```python
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
```

-----

{! content/2021/2021-02-08-serie-evaluacion-perezosa-en-python.txt !}

-----

[genericrange.py]: {attach}/code/2021Q1/lazyseq/genericrange.py "GenericRange class"
[lazyseq.py]: {attach}/code/2021Q1/lazyseq/lazyseq.py "LazySequence class"
[primes.py]: {attach}/code/2021Q1/lazyseq/primes.py "Primes class"
