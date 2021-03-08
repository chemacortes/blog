---
Title: Secuencias infinitas - Evaluación perezosa en python - Parte 2
Date: 2021-02-09 23:21:13
Modified: 2021-03-08 00:05:21
Category: Python
Tags: lazy-eval, sequence, range
Slug: evaluacion-perezosa-en-python-parte-2
Authors: Chema Cortés
Summary: Segunda parte de una serie de artículos dedicados al estudio de la evaluación perezosa en python. En esta parte se estudia las secuencia infintas, algunas implementadas con iteradores, y el modo en que se pueden manejar.
Lang: es
Translation: false
Status:
---

## Algunas definiciones

Puede ser interesante dejar claras algunas definiciones para distinguir entre
iteradores e iterables (se pueden ver las definiciones completas en el
[glosario][] de python):

**Iterable**
: cualquier objeto capaz de devolver sus miembros de uno en uno

**Iterador**
: _iterable_ que representa un flujo de datos, cuyos elementos se
: obtienen uno detrás de otro

**Secuencia**
: _iterable_ con acceso eficiente a sus elementos mediante un índice entero

**Generador**
: función que devuelve un _iterador_

**Expresión generadora**
: expresión que devuelve un _iterador_

Lo importante a tener en cuenta es que tenemos dos grandes _grupos de
iterables_: los _iteradores_ y las _secuencias_.

Los elementos de una _secuencia_ son accesibles por su posición, mientras que
los elementos de un _iterador_ sólo se pueden acceder en serie. _Iterable_ sería
el concepto más general que englobaría ambos términos.

En el resto del artículo hablaremos de _"secuencias"_ como término matemático,
aunque su implementación podría corresponder con cualquier iterable de los
mencionados.

## Secuencias infinitas

En python, para crear secuencias infinitas se suelen usar _generadores_. Por
ejemplo, para obtener la secuencia de _Números Naturales_ se podría hacer así:

```python
from collections.abc import Iterable

def ℕ() -> Iterable[int]:
    n = 0
    while 1:
        yield n
        n += 1
```

No podemos tratar las secuencias infinitas del mismo modo que con una lista.
Necesitamos las funciones del módulo [itertools][] capaces de operar con
iteradores para pasar a una lista en el momento que realmente la necesitemos. Al
final de la documentación del módulo se incluyen algunas
[recetas][itertools-recipes] que dan idea de lo que pueden hacer.

Por ejemplo, podríamos redefinir la secuencia de número naturales con
`itertools.count`:

```python
from itertools import count

ℕ = count(0)
```

Para obtener los primeros 100 números naturales

```python
from itertools import islice

print(list(islice(ℕ, 100)))

[100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199]

```

Emular la función `enumerate`:

```python
from collections.abc import Iterable, Iterator

def enumerate(it: Iterable) -> Iterator:
    ℕ = count(0)
    return zip(ℕ, it)
```

¿Y si quisiéramos obtener la lista de cuadrados en el intérvalo `[100, 200)`.
Veamos (NO PROBAR):

```python
ℕ = count(0)
cuadrados = (n**2 for n in ℕ)
res = [x for x in cuadrados if 100<=x<200]
```

Si probabos es posible que se quede en un bucle infinito. Necesita comprobar
todos los elementos, por lo que se pondrá a calcular todos lo elementos de la
sucesión para ver si cumplen la condición.

Como sabemos que la sucesión de cuadrados es creciente, podemos pararla en el
momento que se salga de límites:

```python
from itertools import dropwhile, takewhile

ℕ = count(0)
cuadrados = (n ** 2 for n in ℕ)
mayores_100 = dropwhile(lambda x: x < 100, cuadrados)
menores_200 = takewhile(lambda x: x <= 200, mayores_100)
res = list(menores_200)
```

En definitiva, hemos encadenado varias funciones hasta conseguir el iterador que
necesitábamos. En _programación funcional_, a este encadenado de funciones se
denomina como _composición de funciones_ y es bastante utilizado.
Lamentablemente, en python no existe este tipo de operaciones.

## Ejemplo: sucesión de Fibonacci

La sucesión de _Fibonacci_ se define de la siguiente manera:

$$f_0=1$$
$$f_1=1$$
$$f_n = f_{n-1} + f_{n-2}$$

Operando, podemos obtener la sencuencia:

```haskell
1
1
1+1 -> 2
1+2 -> 3
2+3 -> 5
...
```

La lista de los 20 primeros:

```python
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
```

Un modo simple de construir la serie es usar un generador:

```python
from collections.abc import Iterator
from itertools import islice

def fib() -> Iterator[int]:
    a, b = 1, 1
    while True:
        yield a
        a, b = b, a+b

# primeros 20 elementos
print(list(islice(fib(), 20)))
```

Para obtener un elemento en una posición dada tenemos que _consumir_ el
iterador, elemento a elemento, hasta llegar a la posición que queremos.

Por ejemplo, para obtener el elemento de la posición 1000:

```python
>>> next(islice(fib(), 1000, None))
70330367711422815821835254877183549770181269836358732742604905087154537118196933
57974224949456261173348775044924176599108818636326545022364710601205337412127386
7339111198139373125598767690091902245245323403501
```

Ha sido necesario calcular todos los elementos anteriores hasta llegar al que
deseamos, algo que hay que repetir para cada uno de los elementos que queramos
extraer.

Afortunadamente, la sucesión de fibonacci tiene elemento genérico que se expresa
en función de el _número áureo_ $\varphi$ y que tiene la siguiente formulación:

$$\varphi ={\frac {1+{\sqrt {5}}}{2}}$$

Usando el _número áureo_, un elemento de la serie fibonacci se puede calcular
con la siguiente fórmula de Édouard Lucas,:

$$f_n=\frac{\varphi^n-\left(1-\varphi\right)^{n}}{\sqrt5}$$

Que podemos ajustar el redondeo y expresar como:

$$f_{n}=\operatorname {int} \left({\frac {\varphi ^{n}}{\sqrt {5}}}+{\frac {1}{2}}\right)$$

Así pues, podemos echar mano de la secuencia `GenericRange` que vimos en el
artículo anterior para definir una secuencia para fibonacci:

```python
class FibRange(GenericRange):
    def getitem(self, n):
        sqrt5 = 5**(1/2)
        φ = (1 + sqrt5) / 2
        return int(φ**n/sqrt5 + 1/2)


>>> list(FibRange(100,110))
[354224848179263111168,
 573147844013818970112,
 927372692193082081280,
 1500520536206901248000,
 2427893228399983329280,
 3928413764606884839424,
 6356306993006868692992,
 10284720757613753532416,
 16641027750620622225408,
 26925748508234379952128]
```

Lamentablemente, aunque al final se obtenga un número entero, para hacer el
cálculo hemos recurrido al cálculo numérico de coma flotante, lo que produce
desbordamiento cuando trabajamos con números grandes. Tenemos que buscar otros
métodos para mantenernos en el dominio de los número enteros. Pero lo dejaremos
ya para el próximo artículo, donde veremos las _memoizaciones_ o el modo de
guardar los resultados de un función para evitar repetir el mismo cálculo cuando
se vuelva a necesitar.

## Resumen

Las secuencias numéricas se pueden expresar en forma de _iterables_, de las que
tenemos dos tipos: `iteradores` y `secuencias`.

Normalmente en python, para trabajar con secuencias infinitas se usan
iteradores. Para poder manejar estos iteradores se usan las funciones del módulo
`itertools` que podemos combinar para obtener como resultado un iterable  que ya
podemos manejar mejor.

Si la secuencia tiene definido un elemento genérico, entonces podemos utilizar
los rangos que ya habíamos visto anteriormente para crear la secuencia infinita.

[glosario]: https://docs.python.org/3.9/glossary.html
[itertools]: https://docs.python.org/3.9/library/itertools.html
[itertools-recipes]: https://docs.python.org/3.9/library/itertools.html#itertools-recipes

-----

{! content/2021/2021-02-08-serie-evaluacion-perezosa-en-python.txt !}

-----
