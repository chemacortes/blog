---
Title: Introducción a la "Evaluación Perezosa" - Evaluación perezosa en python - Parte 1
Date: 2021-02-08 19:17:25
Modified: 2021-03-08 00:04:34
Category: Python
Tags: lazy-eval, sequence, range
Slug: evaluacion-perezosa-en-python-parte-1
Authors: Chema Cortés
Summary: Primera parte de una serie de artículos dedicados al estudio de la evaluación perezosa en python. En esta primera parte se estudia los objetos rango y cómo se pueden generalizar su uso para crear secuencias de la que conocemos cómo calcular un elemento genérico a partir de su posición.
Lang: es
Translation: false
Status:
---

## Introducción a la _Evaluación Perezosa_

Podemos definir _"Evaluación Perezosa"_ como aquella evaluación que realiza los
mínimos cálculos imprecindibles para obtener el resultado final.

La evaluación perezosa es una de las característica del languaje haskell, aunque
vamos a ver que también se puede hacer en otros lenguajes como python.

Por ejemplo, imaginemos que queremos obtener todos los número cuadrados menores
de 100:

```python
cuadrados = [x**2 for x in range(1, 100)]
resultado = [y for y in cuadrados if y < 100]
```

Para obtener el `resultado`, antes hemos calculado la lista completa
`cuadrados`, a pesar de que sólo necesitábamos unos 10 elementos.

Una posible mejora sería usar una expresión generadora:

```python
cuadrados = (x**2 for x in range(1, 100))
resultado = [y for y in cuadrados if y < 100]
```

Aquí los elementos de la lista `cuadrados` se calculan a medida que son
necesarios, sin gastar memoria para almacenar la secuencia a medida que se
obtiene, algo que pasaba con el ejemplo anterior. Aún así, se vuelven a calcular
los 100 cuadrados, ya que no se corta la iteración en ningún momento.
Necesitamos un modo de limitarnos únicamente a los elementos que vamos a
utilizar.

Para quedarnos sólo con los primeros elementos vamos a usar la función
`itertools.takewhile`:

```python
from itertools import takewhile

cuadrados = (x**2 for x in range(1, 100))
resultado = list(takewhile(lambda y: y<100, cuadrados))
```

En este caso, obtenemos únicamente los cuadrados necesarios, lo que supone un
importante ahorro de tiempo de cálculo.

Si no se tiene cuidado, es muy fácil hacer más cálculos de la cuenta, e incluso
acabar en bucles infinitos o agotando los recursos de la máquina. Como veremos
en esta serie de artículos, en python se puede tener evaluación perezosa usando
correctamente iteradores y generadores.

## Tipo Range

Veamos el siguiente código:

```python
>>> r = range(2,100,3)
>>> r[10]
32
```

Normalmente, se usa la función `range` para crear bucles sin tener en cuenta que
realmente es un constructor de objetos de tipo `Range`. Estos objetos responden
a los mismos métodos que una lista, permitiendo obtener un elemento de cualquier
posición de la secuencia sin necesidad de generar la secuencia completa. También
se pueden hacer otras operaciones habituales con listas:

```python
>>> len(r)  # obtener el tamaño
>>> 33
>>> r[20:30]  # obtener un rango
range(62, 92, 3)
>>> r[30:20:-1]  # obtener un rango inverso
range(92, 62, -3)
>>> r[::-1]  # la misma secuencia invertida
range(98, -1, -3)
>>> r[20:30:-1]  # umm, secuencia vacía???
range(62, 92, -3)
>>> r[::2]  # una nueva secuencia con distinto paso
range(2, 101, 6)
>>> 3 in r  # comprobar si contiene un elemento
False
>>> r.index(65)  # buscar la posición de un elemento
21
```

Como vemos, de algún modo calcula los nuevos rangos y los pasos según
necesitemos. Es suficientemente inteligente para cambiar el elemento final por
otro que considere más apropiado.

Digamos que un objeto de tipo `Range` conoce cómo operar con secuencias
aritméticas, pudiendo obtener un elemento cualquiera de la secuencia sin tener
que calcular el resto.

## Secuencias con elemento genérico conocido

Probemos a crear algo similar a `Range` para la secuencia de cuadrados. Derivará
de la clase abstracta `Sequence`, por lo que tenemos que definir, por lo menos,
los métodos `__len__` y  `_getitem__`. Nos apoyaremos en un objeto _range_ para
esta labor (patrón _Delegate_):

```python
from collections.abc import Sequence
from typing import Union


class SquaresRange(Sequence):
    def __init__(self, start=0, stop=None, step=1) -> None:
        if stop is None:
            start, stop = 0, start
        self._range = range(start, stop, step)

    @staticmethod
    def from_range(rng: range) -> "SquaresRange":
        """
        Constructor de SquaresRange a partir de un rango
        """
        instance = SquaresRange()
        instance._range = rng
        return instance

    def __len__(self) -> int:
        return len(self._range)

    def __getitem__(self, idx: Union[int, slice]) -> Union[int, "SquaresRange"]:
        i = self._range[idx]
        return i ** 2 if isinstance(i, int) else SquaresRange.from_range(i)

    def __repr__(self) -> str:
        r = self._range
        return f"SquaresRange({r.start}, {r.stop}, {r.step})"
```

Podemos probar su funcionamiento:

```python
>>> for i in SquaresRange(-10, 1, 3):
...     print(i)
...
100
49
16
1
>>> list(SquaresRange(-1, 50, 4)[:30:2])
[1, 49, 225, 529, 961, 1521, 2209]
>>> SquaresRange(100)[::-1]
SquaresRange(99, -1, -1)
>>> 16 in SquaresRange(-10, 1, 3)
True
```

Hay que tener en cuenta que, a diferencia de un iterador, este rango no se
_"agota"_ por lo que se puede usar repetidas veces sin ningún problema.

Siguiendo más allá, podemos generalizar esta secuencia para se usar cualquier
función. Creamos la siguiente _clase abstracta_:

```python
from abc import abstractmethod
from collections.abc import Sequence
from typing import Type, Union


class GenericRange(Sequence):
    def __init__(self, start=0, stop=None, step=1) -> None:
        if stop is None:
            start, stop = 0, start
        self._range = range(start, stop, step)

    @abstractmethod
    def getitem(self, pos: int) -> int:
        """
        Método abstracto.
          Función para calcular un elemento a partir de la posición
        """
        return pos

    @classmethod
    def from_range(cls: Type["GenericRange"], rng: range) -> "GenericRange":
        """
        Constructor de un GenericRange a partir de un rango
        """
        instance = cls()
        instance._range = rng
        return instance

    def __len__(self) -> int:
        return len(self._range)

    def __getitem__(self, idx: Union[int, slice]) -> Union[int, "GenericRange"]:
        i = self._range[idx]
        return self.getitem(i) if isinstance(i, int) else self.from_range(i)

    def __repr__(self) -> str:
        classname = self.__class__.__name__
        r = self._range
        return f"{classname}({r.start}, {r.stop}, {r.step})"
```

Con esta clase abstracta creamos dos clases concretas, definiendo el método
abstracto `.getitem()` con la función genérica:

```python
class SquaresRange(GenericRange):
    def getitem(self, i):
        return i ** 2

class CubicsRange(GenericRange):
    def getitem(self, i):
        return i ** 3
```

Que podemos emplear de este modo:

```python
>>> for i in SquaresRange(-10, 1, 3):
...     print(i)
...
100
49
16
1
>>> for i in CubicsRange(-10, 1, 3):
...     print(i)
...
-1000
-343
-64
-1
>>> list(CubicsRange(-1, 50, 4)[:30:2])
[-1, 343, 3375, 12167, 29791, 59319, 103823]
>>> SquaresRange(100)[::-1]
SquaresRange(99, -1, -1)
>>> SquaresRange(100).index(91)
9
```

## Resumen

La _Evaluación Perezosa_ realiza únicamente aquellos cálculos que son necesarios
para obtener el resultado final, evitando así malgastar tiempo y recursos en
resultados intermedios que no se van a usar.

El tipo _Range_ es algo más que una facilidad para realizar iteraciones. A
partir de un objeto _range_ se pueden crear nuevos rangos sin necesidad de
generar ningún elementos de la secuencia.

Si conocemos el modo de obtener cualquier elemento de una secuencia a partir de
su posición, entonces podemos crear secuencias para operar con ellas igual que
haríamos con un _rango_, sin necesidad de generar sus elementos.

En el próximo artículo veremos cómo podemos ir más lejos para crear y trabajar
con _secuencias infinitas_ de elementos.

-----

{! content/2021/2021-02-08-serie-evaluacion-perezosa-en-python.txt !}

-----
