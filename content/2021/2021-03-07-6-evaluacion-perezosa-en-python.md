---
Title: Ejemplo práctico. Potencias de Fermi-Dirac - Evaluación perezosa en python - Parte 6
Date: 2021-03-07 23:58:43
Modified: 2021-03-22 00:19:38
Category: Python
Tags: lazy-eval, sequence, range, primes, fermi, dirac
Slug: evaluacion-perezosa-en-python-parte-6
Authors: Chema Cortés
Summary: Visto cómo conseguir secuencias con evaluación perezosa, ya sólo nos falta conocer en qué poder emplearlas. En este artículo veremos las potencias de Fermi-Dirac y cómo las secuencias de evaluación perezosa nos ayudarán a plantear una solución manejable.
Lang: es
Translation: false
Status:
---

Se llaman **potencias de Fermi-Dirac** a los números de la forma $p^{2^k}$,
ordenados de menor a mayor, donde `p` es un número primo y `k` es un número
natural.

Vamos a ver cómo crear la sucesión de `potencias` Fermi-Dirac. Realizaremos las
siguientes comprobaciones:

```python
potencias: list[int]

potencias[:14]    ==  [2,3,4,5,7,9,11,13,16,17,19,23,25,29]
potencias[60]     ==  241
potencias[10**6]  ==  15476303
```

## Estudio previo

Si sacamos la lista de potencias en función del exponente `k` tendríamos las
siguientes sucesiones:

$$
\begin{align*}
P_0 &= 2,3,5,7,11,...\\
P_1 &= 4,9,25,49,121,..\\
P_2 &= 16,81,625,2401,14641,...\\
P_3 &= 256,6561,390625,5764801,214358881,815730721,...
\end{align*}
$$

Necesitamos combinar estas sucesiones en una sola. A priori, no sabemos cuántos
elementos vamos a necesitar de cada sucesión. Como máximo, para sacar las
primeras 14 potencias nos basta con los primeros 14 números primos y crear 14
secuencias, de $P_0$ a $P_{13}$, ordenarlos sus elementos en una única lista y
escoger los primeros 14 elementos. Con este proceso habremos calculado 196
potencias para sólo 14 elementos que necesitamos al final.

```python
from primes import primes

potencias = sorted(p**2**k for p in primes[:14] for k in range(0, 14))
print(potencias[:14])

[2, 3, 4, 5, 7, 9, 11, 13, 16, 17, 19, 23, 25, 29]
```

Aún en el caso de que tuviéramos algún medio de reducir el número de elementos a
usar de cada secuencia, seguimos sin saber cuántos números primos serán
necesarios. Para sacar los 14 primeros elementos de las potencias de Fermi-Dirac
sólo se necesitaban los 10 primeros números primos.

Es evidente que una estrategia por _fuerza bruta_ es complicada y termina por
hacer muchos cálculos innecesarios, una complejidad del $O({n^2})$ no resoluble
con un ordenador normal. Veamos cómo nos puede ayudar la _evaluación perezosa_.

## Modelos

Por intentar crear un modelo, intentemos ver las sucesiones como un iterador de
iteradores:

```python
from itertools import count

from primes import primes

potencias = ((p**2**k for p in primes) for k in count())
```

Pero el problema con las _expresiones generadora_ es similar al que tienen las
expresiones lambda: carecen de su propia clausura y cualquier _variable libre_
queda alterada por el entorno donde se evalúan.

Se puede comprobar el fallo si intentamos extraer dos iteradores:

```python
p0 = next(potencias)
p1 = next(potencias)
next(p1)  # --> 4
next(p0)  # --> 4
next(p0)  # --> 9
```

El exponente `k` ha cambiado de valor con el segundo iterador, lo que afecta a
las potencias del primero. Tenemos que dotar a los iteradores de su propia
clausura:

```python
from collections.abc import Iterator
from itertools import count

from primes import primes

def potencias_gen(k: int) -> Iterator[int]:
    yield from (p**2**k for p in primes)

potencias = (potencias_gen(k) for k in count())
```

Para obtener una única secuencia a partir de este _iterador de iteradores_ en un
único iterador, operación que se conoce como _"aplanar la secuencia"_.

Definimos la siguiente función para mezclar dos listas ordenadas:

```python
# tipo para secuencias ordenadas
SortedIterator = Iterator[int]

def zipsort(s1: SortedIterator, s2: SortedIterator) -> SortedIterator:
    x = next(s1)
    y = next(s2)
    while True:
        if x <= y:
            yield x
            x = next(s1)
        else:
            yield y
            y = next(s2)
```

La función `zipsort` combina dos listas ordenadas `SortedIterator` para devolver
otra lista ordenada `SortedIterator`. Si quisiéramos combinar tres listas,
bastaría con volver repetir con `zipsort`:

```python
zipsort(zipsort(s1, s2), s3)
```

En general, podríamos combinar todas las listas de esta manera:

```python
def flat(iterators: Iterator[SortedIterator]) -> SortedIterator:
    it1 = next(iterators)
    it2 = flat(iterators)
    yield from zipsort(it1, it2)

potencias = flat(potencias_gen(k) for k in count())
```

El problema es que se entra en un bucle infinito de llamadas recursivas a `flat`
que habrá que evitar.

Si observamos las sucesiones $P_0$, $P_1$, $P_2$,..., el primer elemento de una
sucesión es siempre inferior a cualquier elemento de sucesiones posteriores.
Usando esta propiedad, podemos redefinir nuestra función aplanadora:

```python
def flat(iterators: Iterator[SortedIterator]) -> SortedIterator:
    it1 = next(iterators)
    yield next(it1)
    yield from zipsort(it1, flat(iterators))

potencias = flat(potencias_gen(k) for k in count())
```

La función `flat` devuelve siempre un elemento antes de invocarse por
recursividad, suficiente para frenar la cadena de llamadas recursivas. Visto de
otro modo, se ha convertido la función en _perezosa_, devolviendo elementos a
medida que sean necesarios. De todos modos, seguimos limitados por el nivel de
recursividad en python (~3000 niveles en CPython), aunque no vamos a superar
este límite en las pruebas[^1].

## Código final

Descarga: [potencias.py][]

```python
from collections.abc import Iterator
from itertools import count
from typing import TypeVar

from lazyseq import LazySortedSequence
from primes import primes


SortedIterator = Iterator[int]


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
```

Para las comprobaciones:

```python
>>> potencias[:14]
[2, 3, 4, 5, 7, 9, 11, 13, 16, 17, 19, 23, 25, 29]
>>> potencias[60]
241
>>> potencias[10 ** 6]
15476303
>>> primes.size
999432
```

Para obtener el elemento $10^6$ tarda bastante al necesitar obtener casi un
millón de números primos. Una vez obtenidos, el cálculo es bastante rápido.

---

{! content/2021/2021-02-08-0-serie-evaluacion-perezosa-en-python.txt !}

---

ANOTACIONES:

[^1]:
    Es posible que en posteriores artículos veamos técnicas para superar las
    limitaciones de la recursivad en python.

[potencias.py]: {attach}/code/2021Q1/lazyseq/potencias.py "Potencias de Fermi-Dirac"
