---
Title: Evaluación perezosa avanzada - Evaluación perezosa en python - Parte 4
Date: 2021-02-15 21:20:20
Modified: 2021-03-09 02:44:37
Category: Python
Tags: lazy-eval, sequence, range, primes
Slug: evaluacion-perezosa-en-python-parte-4
Authors: Chema Cortés
Summary: Partiendo del algoritmo para la obtención de números primos crearemos una secuencia infinita mediante técnicas de evaluación perezosa que crezca a medida que se necesite. Al final, aplicaremos algunas optimizaciones para el cálculo de números primos.
Lang: es
Translation: false
Status:
---

## _Evaluación perezosa_ avanzada

Haskell tiene una librería, `Data.Numbers.Primes`, que ofrece tanto una
secuencia con todos los números primos, `primes`, como la función `isprime` con
la que chequear si un número es primo. Gracias a la _evaluación perezosa_,
haskell sólo calcula los elementos de `primes` que necesite.

Vamos a intentar hacer en python lo que hace sencillo haskell:

```haskell
> take 100 primes
[2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,
107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,
223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,
337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,
457,461,463,467,479,487,491,499,503,509,521,523,541]

> primes!!90000
1159531

> isPrime (2^31-1)
True
```

## Calculo de números primos

Por definición, un número primo sólo es divisible por `1` y por sí mismo:

```python
Prime = int  # un alias para números primos

def isprime(n: int) -> bool:
    return not any(n % i == 0 for i in range(2, n))

def primes(to: int) -> list[Prime]:
    return [i for i in range(2, to+1) if isprime(i)]
```

Podemos aplicar algunas optimizaciones a estos cálculos:

- Excepto el 2, podemos descartar como primos todos los números pares
- Al comprobar divisores de $n$, basta con probar hasta $\sqrt{n}$, y únicamente
  con aquellos que sean primos

Con estas premisas, podemos ir ya diseñando una estrategia para obtener una
secuencia de primos por evaluación perezosa:

```python
import sys
from collections.abc import Generator, Iterable
from itertools import islice

INFINITE = sys.maxsize  # una aproximación 'mala' para infinito
Prime = int  # un alias para números primos

# lista de números primos que vayamos obteniendo
primes: list[Prime] = [2, 3]


def isdivisible(n: int, divisors: Iterable[int]) -> bool:
    """
    Comprobar si 'n' es divisible por
    los elementos de un iterable ordenado
    """

    divisible = False
    for d in divisors:
        if n % d == 0:
            divisible = True
            break
        if d * d > n:
            break
    return divisible


def isprime(n: int) -> bool:
    """Comprobar si 'n' es un número primo"""

    if n <= primes[-1]:
        return n in primes

    # probando primos como divisores
    if isdivisible(n, primes):
        return False

    # seguir con el resto de números impares
    start = primes[-1] + 2
    return not isdivisible(n, range(start, n, 2))


def genprimes() -> Generator[Prime, None, None]:
    """Generador de números primos"""

    start = primes[-1] + 2
    for n in range(start, INFINITE, 2):
        if not isdivisible(n, primes):
            primes.append(n)
            yield n
```

El generador `genprimes` nos dará un iterador con el que ir obteniendo los
números primos siguientes al último de la lista. A medida que obtiene un primo,
se añade a la lista `primes`.

La lista `primes` actua como _caché_ de los números primos obtenidos y la
empleará `isprime` para sus comprobaciones. Si `isprime` se queda sin primos,
continua con los siguientes números impares hasta obtener un resultado, sin
pararse a calcular los primos intermedios.

## Secuencia de números primos

Vistas estas funciones vamos a armar con ellas la estructura de una clase
_secuencia_. `isprime` pasará a ser el método `__contains__` y el generador
`genprimes` lo usaremos para ampliar automáticamente la lista de números primos
según sea necesario:

```python
import sys
from collections.abc import Generator, Iterable
from itertools import islice
from typing import Union

INFINITE = sys.maxsize  # una mala aproximación de infinito
Prime = int  # un alias para los primos


def isdivisible(n: int, divisors: Iterable[int]) -> bool:
    """
    Comprobar si 'n' es divisible por
    los elementos de un iterable ordenado
    """

    divisible = False
    for d in divisors:
        if n % d == 0:
            divisible = True
            break
        if d * d > n:
            break
    return divisible


def nth(it: Iterable, n: int):
    """Obtener de un iterable el elemento en la posición 'n'"""
    return next(islice(it, n, None))


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
        """Comprobar si 'n' es un número primo"""

        if n <= self.last:
            return n in self._primes

        # probando primos como divisores
        if isdivisible(n, self._primes):
            return False

        # seguir con el resto de números impares
        start = self.last + 2
        return not isdivisible(n, range(start, n, 2))

    def genprimes(self) -> Generator[Prime, None, None]:
        """Generador de números primos"""

        start = self.last + 2
        for n in range(start, INFINITE, 2):
            if not isdivisible(n, self._primes):
                self._primes.append(n)
                yield n

    def __getitem__(self, idx: Union[int, slice]) -> Prime:
        if isinstance(idx, int):
            if idx < 0:
                raise OverflowError

            return (
                self._primes[idx]
                if idx < self.size
                else nth(self.genprimes(), idx - self.size)
            )
        else:
            rng = range(INFINITE)[idx]
            return [self[i] for i in rng]

# Secuencia de los números primos
primes = Primes()
isprime = primes.__contains__
```

Como _infinito_ se usa `sys.maxsize` que es el mayor tamaño que puede tener una
lista para la versión `CPython`. Si tratamos de usar índices mayores para una
lista nos dará error.

Cuando se solicita un número primo que no está en la lista, el método
`__getitem__` invoca automáticamente al iterador que devuelve `genprimes` hasta
alcanzarlo. A medida que se descubren números primos, se val almacenando para su
posterior uso.

Pruebas de uso:

```python
>>> from primes import primes, isprime
>>> print(primes[:100])
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73,
 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157,
 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241,
 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347,
 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439,
 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541]
>>> primes[90000]
1159531
>>> isprime(2**31-1)
True
>>> (2**31-1) in primes._primes
False
>>> primes.last
1159531
```

Para cumplir con el protocolo `Sequence` podemos añadir los métodos que nos
faltan, cosa que animo hacer al lector. El método `count()` es trivial: si es
primo, habrá 1 ocurrencia; si no es primo, 0 ocurrencias. El método `index()` es
algo más complicado. En cambio el `_reversed__()` es imposible ya que no se
puede invertir una secuencia infinta. A pesar de ello, la clase `Prime` se
comportará casi como una secuencia siempre y cuando no itentemos acceder a la
secuencia por el final.

## Más optimizaciones

### Bisecciones

La lista de primos que vamos generando siempre será una _lista ordenada_, por lo
que se pueden optimizar mucho las búsquedas usando _bisecciones_, para lo que
tenemos el módulo `bisect` ($O(\log{n})$ en lugar de $O(n)$).

Por ejemplo, para comprobar si un elemento está en una lista ordenada:

```python
from bisect import bisect_left

def bs_contains(lst: list, x) -> bool:
    idx = bisect_left(lst, x)
    return idx < len(lst) and lst[idx] == x
```

### Programación dinámica

En el generador de números primos podemos observar que se están comprobando los
cuadrados de los divisores más veces de las necesarias. Podemos delimitar rangos
en los que se van a usar los mismos divisores. Por ejemplo, si tenemos la
secuencia `[2, 3]` como divisores podemos chequear números hasta el `23`. Para
seguir con el `25` tenemos que añadir un primo más, `[2, 3, 5]` con los que ya
podemos chequear hasta el `47`. Y así sucesivamente. El rango `range(start,
INFINITE, 2)` lo podemos fraccionar según el grupo de primos que emplearemos
como divisores.

La _programación dinámica_ tiene sus riesgos y es bastante fácil que no funcione
bien a la primera, pero mejoran mucho la eficiencia de un algoritmo.

### Multiproceso

Como opción de mejora está el uso de técnicas de concurrencia y multiproceso.
Como primera medida que podemos pensar sería crear varios _workers_ que chequeen
en paralelo la divisibilidad para chequear varios números a la vez. El problema
es que estos workers tendrían que tener su copia de la lista de primos y
actualizarla conforme se obtenien, algo que es sumamente costoso y poco
eficiente.

Una estrategia mejor sería especializar cada _worker_ en un subconjunto de
números primos de modo que todos los _workers_ intervengan colaborativamente en
el chequeo del mismo número.

En concurrencia, hay muchas estrategias posibles y ninguna mejor. Al final, cada
problema tiene su solución particular que no sirve como solución general.

### Código final optimizado

El código final optimizado, sin usar concurrencia, se puede obtener del
siguiente enlace:

!!! Descarga
    [primes.py]({attach}/code/2021Q1/old/primes.py)

Por hacernos una idea, esta sería la comparativa de tiempos de la versiones haskell y python:

<!-- markdownlint-disable MD033 -->
<style>
table, th, td { border: 1px solid grey;padding: 1.2em;}
table {border-collapse: collapse;}
</style>
<!-- markdownlint-enable MD033 -->

| operación          | haskell | python | python opt |
|:-------------------|--------:|-------:|-----------:|
|primo 90000         | 310ms   | 1450ms | 860ms      |
|es primo $2^{31}-1$ |  20ms   |   10ms |   3ms      |
|index 1159531       | 240ms   |    N/A | 820ms      |

-----

{! content/2021/2021-02-08-serie-evaluacion-perezosa-en-python.txt !}

-----
