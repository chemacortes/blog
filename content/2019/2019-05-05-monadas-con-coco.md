---
Title: Monadas con coco
Date: 2019-05-07 19:33:19
Modified: 2019-05-07 19:47:56
Category: Coconut
Tags: coconut, functional-programming, python
Slug:
Authors: Chema Cortés
Summary: Los iterables han dejado la programación funcional para ser parte de los lenguajes de programación modernos. Veremos cuáles son las implementaciones en python y coconut, y las diferencias entre ellos.
Lang: es
Translation: false
Status:
---

!!! hint "🥥=🐍+🐒"

## Iterables

Si duda los **Iterables** es la característica de programación funcional que más se usa en python. Se emplean en las *compresiones de listas* y las *expresiones generadoras*.

Pero veamos algunas definiciones:

- **Iterable**: objeto del que se puede recorrer sus elementos en orden, uno a uno. Como ejemplos, están los tipos `list`, `str`, `tuple` y `dict`. Lo común es recorrer sus elementos con un bucle `for`.
- **Iterador**: objeto que representa un flujo de datos. Con cada uso, o bien entrega un dato, o bien produce una excepción por quedarse vacío. Por diseño, un `Iterador` deriva de `Iterable`.
- **Secuencia**: *iterable* con acceso a la posición de cualquiera de sus elementos y con un tamaño conocido. Como ejemplos están los tipos `list`, `str` y `tuple`. El tipo `dict` también funciona como secuencia, pero no se considera como tal al no accederse a sus elementos por posición numérica. (Es más considerado como *mapping*).
- **Generador**: objeto que crea iteradores. Hay *funciones generadoras*, que crean un iterador cada vez que se llaman, y *expresiones generadoras*, que crean un sólo iterador.

*Iteradores* y *secuencias* forman el conjunto de los *iterables*, y podemos identificarlos estructuralmente de la siguiente manera:

- Un **Iterable** suele tener un método `__iter__` que devuelve un iterador para recorrer en orden todos los elementos.
- Un **Iterador** tiene un método `__next__` para entregar el siguiente dato.
- Una **Secuencia** tiene un método `__getitem__`, para acceso a cualquier elemento, y un método `__len__`, para conocer su tamaño. Además, pueden tener otros métodos como `count()`, `index()`, `__contains__()` y `__reversed__()` con los que completar la *clase base abstracta* [collections.abc.Sequence](https://docs.python.org/3.7/library/collections.abc.html#collections.abc.Sequence).

!!! Important "Importante"
    Aunque un *Iterable* se suele caracterizar por tener un método `__iter__`, también las *secuencias* se consideran *iterables* aunque no tengan este método.

Caso práctico: analicemos un objeto `range` (eg: `dir(range(10))`):

- tiene el métodos `__iter__` --> es un `Iterable`
- tiene los métodos `__getitem__` y `__len__` --> es una `Secuencia`
- tiene el resto de métodos de `collections.abc.Sequence`
- no tiene método `__next__`

Los objeto `Range` son *secuencias*, no *iteradores*. Como secuencia, algunas de la operaciones que permite son:

- troceo: `range(100)[4:20] == range(4,20)`
- obtener el tamaño: `len(range(100)) == 100`
- chequeos de pertenencia: `200 in range(100) == False`
- inversión: `range(100)[::-1] == range(99, -1, -1)`

## Composición de Iteradores

Una ventaja de usar iteradores en lugar de listas es que sólo necesitan memoria para procesar el elemento que están trabajado, por lo que los hace muy eficientes para procesar grandes cantidades de datos o ficheros enormes que no caben enteros en memoria.

Por ejemplo, esta expresión generadora:

~~~.python
(x**2 for x in range(10**100))
~~~

Como curiosidad, el número `10**100` se llama [gúgol](https://es.wikipedia.org/wiki/Gúgol) y es un número enormemente grande. Crear esto mismo como una lista es imposible con la memoria de los ordenadores actuales y no habría tiempo en este Universo para procesar tal cantidad de elementos.

Y sin embargo, podemos trabajar con esta expresión sin mayores problemas. Por ejemplo, para obtener los 10 primeros elementos:

~~~.python
g = (x**2 for x in range(10**100))
for i in range(10):
    print(next(g))
~~~

Incluso podemos usarla como base para crear nuevos iteradores:

~~~.python
(y+1 for y in (x**2 for x in range(10**100)))
~~~

Equivalente a hacer:

~~~.python
(x**2+1 for x in range(10**100))
~~~

Componer iteradores es bastante eficiente. Se van recorriendo a medida que sea necesario, sin mantener en memoria nada más que los elementos estrictamente necesarios para devolver el siguiente elemento.

## map y filter

¿Sabes cuál es la diferencia entre estas dos expresiones?

~~~.python
(x**2 for x in range(10*100))

map(lambda x: x**2, range(10*100))
~~~

Para python, ambas expresiones son equivalentes: iteradores. Pero se considera que tiene más *estilo pythónico* el uso de expresiones generadoras, desaconsejándose completamene el uso de las funciones `map` y `filter` siempre que se pueda.

Y sin embargo, para *coconut* las funciones `map` y `filter` son fundamentales como también lo son en *programación funcional*.

El iterador que se obtiene con la expresión generadora `(x**2 for x in range(10*100))` actúa como si fuera una *caja negra*. Se pueden obtener los elemntos uno a uno, pero no ofrece información sobre su estructura interna, ni de su tamaño, ni nada que permita su transfomación.

En cambio, el *iterador map* en coconut (extensión de la función `map` de python) almacena información tanto de la función como de los iterables a los que se aplica, cosa que hace en los atributos `func` y `iters`, respectivamente. De este modo, *coconut* puede encadenar transformaciones de manera más óptima.

Por ejemplo, para obtener el último elemento del iterador anterior:

~~~.coconut
map(x -> x**2, range(10*100))[-1]
~~~

Como iterador, debería haber pasado por todos los `10**100` elementos hasta llegar al último, cosa que es imposible de hacer en la práctica. Sin embargo, si se prueba en *coconut*, se obtiene el último elemento casi al instante. En realidad, *coconut* cortocircuita todo el proceso y salta directamente al último elemento de `range(10**100)`, que es el único que le hace falta. Es como si hubiera aplicado primero el `[-1]` al `range(10**100)` y luego hubiera aplicado el `map`.

Este tipo de encapsulado, tanto de un conjunto de datos como de la función que lo transforma, se conocen por **aplicativo** (*Applicative* en inglés). Y a las transformaciones que podemos encadenar, una tras otra, para diferir el cálculo al final del todo se conoce por **mónadas** (*Monad* en inglés).

Más adelante veremos una definición matemática formal, pero podemos considerar **monad** como la *herramienta matemática* más poderosa de un programador funcional y, algunas veces, también la más incomprensible.
