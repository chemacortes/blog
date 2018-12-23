Title: Estudio función factorial en scala - Revisión funcional
Date: 2012-02-07 13:41
Author: Chema Cortés
Category: Scala
Tags: algorithm, factorial
Slug: estudio-funcion-factorial-en-scala-revision-funcional

Como programador de python que todavía anda algo despistado estudiando scala, ahora empiezo a captar la filosófía que hay detrás de este lenguaje de programación. Mientras que python empienza a erradicar poco a poco la programación funcional, en scala su influencia es cada vez mayor hasta el extremo de considerar precindibles la mayoría de los bucles. Aún asi, ambos lenguajes soportan la *"compresión de listas"* como técnica a medio camino entre funcional y bucle estándar, aunque esta técnica está más orientada a obtener listas a partir de otras listas, y no para realizar cálculos sobre un conjunto de números.

Voy a completar el anterior artículo que trataba del ["Estudio función factorial en scala"][1] con algunas formas más *"funcionales"* de definir el factorial:

[1]: {filename}estudio-funcion-factorial-en-scala.md

La forma más simple de definir la función factorial:

```scala
def fact(n:Int) = (1 to n).product
```

En realidad, `1 to n` no es un elemento sintáctico del lenguaje, si no más bien la forma *alternativa* de escribir la invocación del método `1.to(n)`. Este método nos genera una secuencia de números desde el 1 al n (equivalente en python a range(1,n+1)).

Curiosamente, también está definido `fact(0)` gracias a que `product` da como resultado el elemento neutro `1` en secuencias vacías [^1].

Esta forma concisa de calcular el producto es común a todas las secuencias en scala. Faltaría, tan sólo, que operara con BigInts para que fuera perfecta:

```scala
def fact(n:Int) = (BigInt(1) to n).product
```

No es necesario indicar el tipo devuelto por la función puesto que el compilador es capaz de inferirlo de la expresión.

Otra forma funcional sería usando el método `reduce`, donde se indica *explícitamente* la operación binaria a realizar entre pares de elementos:

```scala
def fact(n:Int) = (BigInt(1) to n).reduce(_*_)
```

Como operación se pone una especie de *plantilla* (*pattern*) que representa la operación binaria de multiplicación. Por comparar, en python se puede hacer algo así:

```python
from operator import __mul__

def fact(n):
   return reduce(__mul__, xrange(1,n+1))
```

Lamentablemente, el operador funcional `'reduce'` está desapareciendo de python por considerarlo complejo de entender en su funcionamiento [^2].

Por último, aún existe otra forma funcional de expresar el factorial en scala. Son los *"plegados"* (*folds*), similar en funcionamiento a `reduce`, pero con control sobre la dirección del recorrido y la posibilidad de dar un valor inicial:

```scala
def fact(n:Int) = (1 to n).foldLeft(BigInt(1))(_*_)
```

Seguro que pronto se me ocurrirán más formas.

[^1]: En el caso del método `sum` daría el elemento neutro para la suma, o sea, el `0`.
[^2]: Personalmente, considero que la desaparición de la programación funcional se debe más a la corta visión de quién sólo ve un encadenamiento de sentencias, en lugar de ver *"actores"* interaccionando en libre concurrencia.
