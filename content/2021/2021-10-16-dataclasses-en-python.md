---
Title: Dataclasses en python
Date: 2021-10-17 12:00:00
Modified: 2021-10-17 12:40:03
Category: Python
Tags: dataclass
Slug: dataclasses-en-python
Authors: Chema Cortés
Summary: Aunque para python sea algo nuevo, las _dataclasses_ son bastante comunes en muchos lenguajes funcionales. No es una implementación tan completa, pero ofrece ventajas que pueden ahorrar bastante trabajo.
Lang: es
Translation: false
Status:
---

## Qué son las Dataclasses

Aunque para python sea algo nuevo, las _dataclasses_ son bastante comunes en
muchos lenguajes funcionales. Permiten crear _tipos de datos estructurales_ con
algunas características implementadas por defecto como la _comparación_, la
_ordenación_ o la _descomposición_.

Lamentablemente, la implementación que se incluye a partir de python 3.7 se
queda algo corta y tiene pintas de que tendrá que revisarse en el futuro. Para
una implementación más completa y estable se cuenta con la librería [attr.s][],
compatible con más versiones de python, como PyPy o CPython 2.7, y cuyos
desarrolladores contribuyeron a que el módulo estándar [dataclasses][] tuviera
un mínimo de usabilidad, aunque no fuera lo que hubieran deseado.

Una _dataclase_ se puede considerar como una clase especializada en guardar
estados, en vez de ser una representación de la lógica de la aplicación como
siempre se ven las clases. Con las _dataclases_ se pueden crear tipos de datos
similares a los algebráicos en lo que respecta a las operaciones que se pueden
hacer con ellos: comparar, ordenar, imprimir, indexar, inmutabilidad, etc.
Muchas de estas características están implementadas por los llamados _métodos
mágicos_ ó _métodos especiales_ de python (eg: `__add__` para implementar la
suma). Estos _métodos mágicos_ se pueden agrupan para definir los llamados
_protocolos_ (eg: protocolo _Iterador_), de los que ya he hablado en algún
artículo.

## Comparando clases

Por empezar a ver algún ejemplo, supongamos que definimos una clase para los
puntos en el plano:

```python
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
```

Para que muestre una representación legible, implementamos el método `__repr__()`:

```python
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x:.1f}, y={self.y:.1f})"
```

Probamos:

```python
>>> Point(1, 2)
Point(x=1.0, y=2.0)
```

Para poder comparar si dos puntos son iguales tenemos que añadir el método `__eq__`:

```python
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x:.1f}, y={self.y:.1f})"

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
```

De este modo podemos hacer comprobaciones como `Point(1.0, 2.0) != Point(2.0,
1.0)`. En realidad, para comprobar que no son iguales existe otro método
específico, `__ne__()`, pero a falta de aquél se emplea `__eq__()` de modo
equivalente.

Para comprobar si un punto es mayor o menor habría que implementar también los
métodos `__lt__()`, `__le__()`, `__gt__()` y `__ge__()`, correspondientes a las
operaciones `<`, `<=`, `>` y `>=` respectivamente. Bastaría con sólo una de
estas operaciones y el método `__eq__()` para implementar el resto de métodos,
que es precisamente lo que hace el decorador `functools.total_ordering`:

```python
from functools import total_ordering

@total_ordering
class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point(x={self.x:.1f}, y={self.y:.1f})"

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)

    def __lt__(self, other):
        return (self.x, self.y) < (other.x, other.y)
```

El decorador `total_ordering` creará el resto de métodos de comparación que
faltan a partir de `__eq__()` y `__lt__()`. Lamentablemente, sobrecarga bastante
la clase debido a las dependencias que establece entre métodos, lo que baja
bastante el rendimiento de nuestro código.

Se podrían seguir añadiendo manualmente más métodos para definir otras
operaciones. El mayor incoveniente que vamos a tener, además de bajar el
redimiento, es que a medida que añadimos métodos se complica más y más el
mantenimiento. Si, por ejemplo, quisiéramos añadir un nuevo atributo supondría
cambiar casi todos los métodos.

## Dataclases

Las _dataclases_ en python es una mejora del decorador
`functools.total_ordering`. El decorador `dataclass` definirá por nosotros
varios de de los _métodos mágicos_ más comunes, pero sin establecer dependencias
entre métodos tal como hacía `functools.total_ordering`.

Por ejemplo, la clase `Point` se podría haber construido de esta manera:

```python
from dataclasses import dataclass

@dataclass(order=True)
class Point:
    x: float
    y: float
```

Por defecto, nos construye los métodos `__init__()`, `__repr__()` y `__eq__`
para inicializar, representar y comparar. Con el parámetro `order=True` le
pedimos, además, que nos cree los métodos de ordenación, tal como hacía
`functools.total_ordering`.

Hay más parámetros para controlar la creación de estos métodos y que conviene
consultar en la [documentación][dataclasses]. Vamos a ver algunas de las
facilidades que ofrece:

### Atributos + Representación + Comparación

Como ya hemos comentado, por defecto se crean los métodos para inicializar, representar y comparar.

```python
@dataclass
class Point:
    x: float
    y: float
```

Por defecto, se pueden reasignar el valor de los atributos (_mutable_) y acceder
a estos atributos mediante la notación _dot_:

```python
>>> c = Point(1, 2)
>>> c
Point(x=1, y=2)
>>> c.x
1
>>> c.y
2
>>> c == Point(2, 1)
False
```

A los atributos se pueden asignar valores por defecto y hacerlos inmutables
(como si fueran _propiedades_) que se explicar en la [documentación del
módulo][dataclasses].

### Ordenación

Como ya hemos visto, se pueden crear los métodos de ordenación que equivalen a
las operaciones `<`, `<=`, `>` y `>=`:

```python
@dataclass(order=True)
class Point:
    x: float
    y: float
```

### Hashable y Mutable

Podemos hacer que las instancias sean _hashables_, o sea, que tengan un _hash_
que las identifique (casi)unívocamente:

```python
@dataclass(unsafe_hash=True)
class Point:
    x: float
    y: float
```

Como hemos dicho, una instancia _dataclass_ es por defecto _mutable_, por lo que
no es seguro usar este _hash_ en ciertos usos como, por ejemplo, para índice
de un diccionario.

### Hashable e Immutable

Para tener un _hash_ más seguro, podemos usar el parámetro `frozen`:

```python
@dataclass(frozen=True)
class Point:
    x: float
    y: float
```

En este caso, las instancias son inmutables una vez que han sido creadas y se
puede usar perfectamente como índices de diccionarios.

### Descomposición

Tal vez sea la _descomposición_ o _desestructuración_ de una _dataclase_ la
característica que más se echa en falta en esta implementación de python.

Si funcionara, podríamos hacer cosas tales como:

```python
# OJO: ESTE CÓDIGO NO FUNCIONA
>>> p = Point(1, 2)
>>> Point(a, b) = p
>>> a
1
>>> b
2
```

Pero donde mejor se ve su potencial sería en combinación con la sentencia
`match` (_python 3.10_):

```python
# OJO: ESTE CÓDIGO NO FUNCIONA
match p:
    case Point(0, y):
        print(f"Eje de coordenadas: {y}")
    case Point(x, 0):
        print(f"Eje de abcisas: {x}")
    case Point(x, y):
        print(f"Fuera de ejes: ({x}, {y})")
```

Para tener algo "parecido", se puede transformar la instancia _dataclass_ en una
tupla o un diccionario usando las funciones `dataclasses.astuple` o
`dataclasses.asdict` y usar las asignaciones típicas de estos tipos:

```python
>>> from dataclasses import astuple, asdict
>>> p = Point(1, 2)
>>> (a, b) = astuple(p)
>>> a
1
>>> b
2
```

Podemos ir más allá e implementarlo en la misma clase:

```python
from dataclasses import dataclass, astuple

@dataclass(order=True)
class Point:
    x: float
    y: float

    def __iter__(self):
        yield from astuple(self)

    def __getitem__(self, keys):
        return iter(getattr(self, k) for k in keys)
```

Probamos:

```python
>>> p = Point(1, 2)
>>> (a, b) = p
>>> a
1
>>> b
2
>>> (x, y) = p["x", "y"]
>>> (x, y)
(1, 2)
```

### Optimización

Un último truco: como todos los atributos van a estar declarados en la
definición de la clase, se puede hacer uso del atributo `__slots__` para evitar
la creación del diccionario del objeto, lo que puede suponer un ahorro de
memoria significativo en el caso de que se vaya a usar esta clase para carga
masiva de datos:

```python
from dataclasses import dataclass, astuple

@dataclass(order=True)
class SlottedPoint:
    __slots__ = ["x", "y"]
    x: float
    y: float

    def __iter__(self):
        yield from astuple(self)
```

Si comparamos tamaños:

```python
>>> import sys
>>> sys.getsizeof(Point)
1064
>>> sys.getsizeof(SlottedPoint)
896
```

En ciertas circunstancias, el uso de `__slots__` aumenta la velocidad de
creación de instancias y el acceso a sus atributos. Por contra, no permite dar
valores por defecto a los atributos.

[dataclasses]: https://docs.python.org/3/library/dataclasses.html "dataclasses — Data Classes"
[attr.s]: https://www.attrs.org "attrs: Classes Without Boilerplate"
