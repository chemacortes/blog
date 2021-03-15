---
Title: Evaluación perezosa en python - Apéndice
Date: 2021-03-10 23:55:43
Modified: 2021-03-15 20:55:00
Category: Python
Tags: lazy-eval, sequence, range
Slug: evaluacion-perezosa-en-python-apendice
Authors: Chema Cortés
Summary: Una revisión crítica al tipado gradual de datos de python que se ha usado en esta serie de artículos sobre _evaluación perezosa_.
Lang: es
Translation: false
Status:
---

## Apéndice: sobre el tipado de datos utilizado

Durante esta serie de artículos he procurado usar el _tipado gradual_ de python,
no sólo para mejorar la compresión, sino porque lo considero buena práctica para
detectar algunos problemas en el momento de escribir el código. El intérprete de
python realmente no realiza ningún chequeo de estas _anotaciones_ de tipos,
dejando por completo su comprobación a alguna otra herramienta que pueda estar
usando el desarrollador.

He utilizado las clases abstractas del módulo `collections.abc` como base para
definir los _iterables_, _secuencias_ e _iteradores_. He creído que así quedaba
mejor documentado, además de ser el modo más conocido por programadores de otros
lenguajes. Por derivar de la clase abstracta `Sequence`, sabemos que
`GenericRange` implementa varios métodos abstractos como son `__len__` y
`__getitem__`.

Sin embargo, en python se considera supérfluo y poco recomendable este uso de
clases abstractas. El modo _pythónico_ consiste en implementar esos métodos sin
más indicación. Sólo por el hecho de contar con estos métodos, nuestra clase ya
será considerada como _secuencia_, se podrá usar donde haga falta una
_secuencia_ y, en definitiva, se comportará como si fuera una secuencia. Son los
llamados _duck types_ o _tipos estructurales_ que tanto caracterizan a python y
que, a partir de ahora, nos vamos a tener que acostumbrar a denominar
**_Protocolos_**.

Por ejemplo, podíamos haber declarado la clase `GenericRange` sin indicar
ninguna superclase:

```python
class GenericRange:
    def __init__(self, start=0, stop=None, step=1) -> None:
        ...

    def __len__(self) -> int:
        ...

    def __getitem__(self, idx: Union[int, slice]) -> Union[int, "GenericRange"]:
        ...
```

Al tener el método `__len__()` se dice que cumple con el _protocolo `Sized`_,
algo que se puede comprobar del mismo modo que si fuera una subclase:

```python
>>> from collections.abc import Sized
>>> issubclass(GenericRange, Sized)
True
```

En cambio, nos puede sorprender que no cumpla con el _protocolo `Sequence`_, a
pesar de que se comportaba como tal:

```python
>>> from collections.abc import Sequence
>>> issubclass(GenericRange, Sequence)
False
```

Resulta que para cumplir con el protocolo `Sequence`, además de `__getitem__()`,
debe tener implementados los métodos  `__iter__()`, `__reversed__()` e
`index()`.

Cuando `GenericRange` derivaba de `Sequence`, estos métodos se heredaban de la
superclase como _métodos mixin_, para cuya implementación básica utiliza
únicamente el método `__getitem__()`. También implementa otros métodos como
`__contains__()` (_Container_) y `count()` (_Countable_). Ése era el motivo por
el que sólo hacía falta definir `__getitem__()` para que funcionara como
secuencia.

Como _protocolo_, estos métodos no se adquieren por herencia y necesitan una implementación para cumplir con el protocolo `Sequence`. No obstante, algunas funciones, como `reversed`, admiten objetos con implementaciones parciales del protocolo `Sequence`, algo que únicamente sabremos si recurrimos a la documentación de la función.

## Secuencia de enteros

He empleado el tipo `Sequence` sin indicar de qué tipo son los elementos. Un
chequeador de tipos asume que se trata de un iterable de elementos de tipo
`Any`, por lo que no debería dar problemas. Pero siempre podemos ser más
precisos y usar `Sequence[int]` como tipo de datos para nuestras secuencias de
números enteros.

## Referencia _forward_

En la anotaciones de tipos, a veces necesitamos referenciar una clase antes de
que esté definida, las conocidas como _referencias forward_ de tipos. El modo
normal de hacer este tipo de referencias es escribir el nombre de la clase entre
comillas, como una _string_.

A partir de python 3.10 no hará falta acudir a este remedio pudiendo usar
referencias _forward_ sin mayor problema. Para las versiones anteriores, se
puede obtener esta funcionalidad del módulo `__future__`:

```python
from __future__ import annotations
```

## Unión de tipos

En el método `__getitem__()` de `GenericRange` he utilizado dos uniones de tipos:

```python
    def __getitem__(self, idx: Union[int, slice]) -> Union[int, "GenericRange"]:
        i = self._range[idx]
        return self.getitem(i) if isinstance(i, int) else self.from_range(i)
```

La unión `idx: Union[int, slice]` se puede interpretar como que `idx` puede ser
de tipo `int` o de tipo `slice`. La notación común de expresar esta unión de
tipos en varios lenguajes sería `idx: int | slice`, nomenclatura que también
será aceptada en python 3.10.

La otra unión, `Union[int, "GenericRange"]` indica que el resultado será de tipo
`int` o de tipo `GenericRange`.

De todos modos, en estas anotaciones no se está reflejando la dependencia que
hay entre tipos. Si `idx` es entero, el resultado siempre será un entero. Si
`idx` es `slice`, el resultado siempre será `GenericRange`. En lenguajes con
tipado estático, es normal disponer de varias definiciones del mismo métodos,
con diferentes signaturas, que se seleccionan según sean los tipos de los
argumentos y resultados que tengamos.

Python tiene una facilidad para hacer algo similar. Con
`functools.singledispathmethod` podemos definir varios métodos que se invocarán
según el tipo de dato del primer argumento. De este modo, el método
`__getitem__()` lo podríamos expresar así:

```python
from functools import singledispatchmethod

class GenericRange(Sequence):
    ...

    @singledispatchmethod
    def __getitem__(self, idx):
        return NotImplemented

    @__getitem__.register
    def _(self, idx: int) -> int:
        i = self._range[idx]
        return self.getitem(i)

    @__getitem__.register
    def _(self, idx: slice) -> "GenericRange":
        i = self._range[idx]
        return self.from_range(i)
```

Lamentablemente nos saldrá un error ya que no existe aún la clase `GenericRange`
cuando es aplicado el decorador `singledispatchmethod`. Una solución es sacar el
último registro fuera, una vez que ya se ha definido la clase:

```python
@GenericRange.__getitem__.register
def _(self, idx: slice) -> GenericRange:
    i = self._range[idx]
    return self.from_range(i)
```

## Código final

Con estos cambios, tendríamos nuestro código corregido de esta manera:

```python
from abc import abstractmethod
from collections.abc import Sequence
from typing import Type, Union
from functools import singledispatchmethod
from __future__ import annotations

class GenericRange(Sequence[int]):
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
    def from_range(cls: Type[GenericRange], rng: range) -> GenericRange:
        """
        Constructor de un GenericRange a partir de un rango
        """
        instance = cls()
        instance._range = rng
        return instance

    def __len__(self) -> int:
        return len(self._range)

    @singledispatchmethod
    def __getitem__(self, idx):
        return NotImplemented

    @__getitem__.register
    def _(self, idx: int) -> int:
        i = self._range[idx]
        return self.getitem(i)

    def __repr__(self) -> str:
        classname = self.__class__.__name__
        r = self._range
        return f"{classname}({r.start}, {r.stop}, {r.step})"


@GenericRange.__getitem__.register
def _(self, idx: slice) -> GenericRange:
    i = self._range[idx]
    return self.from_range(i)
```

## Conclusión

Python está realizando un gran esfuerzo en incorporar _anotaciones de tipo_ sin
perder con ello sus característicos tipos _ducking_. De igual modo, vamos a ver
cómo se incorporan más elementos de otros lenguajes como las _dataclasses_,
_programación asíncrona_ o los _patrones estructurales_, aunque tardarán en ser
adoptados por la mayor parte de programadores python.

Si algo tiene python es no tener demasiada prisa en que se apliquen sus cambios.
Como decía un gran sabio: _"Vamos a cambiarlo todo para que todo siga igual"_.

-----

{! content/2021/2021-02-08-0-serie-evaluacion-perezosa-en-python.txt !}

-----
