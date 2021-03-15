---
jupyter:
  authors:
  - "Chema Cort\xE9s"
  description: "Serie de art\xEDculos sobre la implementaci\xF3n en python de secuencias\
    \ con evaluaci\xF3n perezosa."
  jupytext:
    formats: ipynb,md
    notebook_metadata_filter: authors,title,description,toc
    split_at_heading: true
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.10.3
  kernelspec:
    display_name: Python 3
    language: python
    name: python3
  title: "Evaluaci\xF3n Perezosa en python"
  toc:
    base_numbering: 1
    nav_menu: {}
    number_sections: true
    sideBar: true
    skip_h1_title: false
    title_cell: Tabla de Contenidos
    title_sidebar: Contenidos
    toc_cell: true
    toc_position: {}
    toc_section_display: true
    toc_window_display: true
---

<!-- #region toc=true -->
<h1>Tabla de Contenidos<span class="tocSkip"></span></h1>
<div class="toc"><ul class="toc-item"><li><span><a href="#Introducción-a-la-Evaluación-Perezosa" data-toc-modified-id="Introducción-a-la-Evaluación-Perezosa-1"><span class="toc-item-num">1&nbsp;&nbsp;</span>Introducción a la <em>Evaluación Perezosa</em></a></span><ul class="toc-item"><li><span><a href="#Tipo-Range" data-toc-modified-id="Tipo-Range-1.1"><span class="toc-item-num">1.1&nbsp;&nbsp;</span>Tipo Range</a></span></li><li><span><a href="#Secuencias-con-elemento-genérico-conocido" data-toc-modified-id="Secuencias-con-elemento-genérico-conocido-1.2"><span class="toc-item-num">1.2&nbsp;&nbsp;</span>Secuencias con elemento genérico conocido</a></span></li><li><span><a href="#Resumen" data-toc-modified-id="Resumen-1.3"><span class="toc-item-num">1.3&nbsp;&nbsp;</span>Resumen</a></span></li></ul></li><li><span><a href="#Secuencias-infinitas" data-toc-modified-id="Secuencias-infinitas-2"><span class="toc-item-num">2&nbsp;&nbsp;</span>Secuencias infinitas</a></span><ul class="toc-item"><li><span><a href="#Algunas-definiciones" data-toc-modified-id="Algunas-definiciones-2.1"><span class="toc-item-num">2.1&nbsp;&nbsp;</span>Algunas definiciones</a></span></li><li><span><a href="#Secuencias-infinitas" data-toc-modified-id="Secuencias-infinitas-2.2"><span class="toc-item-num">2.2&nbsp;&nbsp;</span>Secuencias infinitas</a></span></li><li><span><a href="#Ejemplo:-sucesión-de-Fibonacci" data-toc-modified-id="Ejemplo:-sucesión-de-Fibonacci-2.3"><span class="toc-item-num">2.3&nbsp;&nbsp;</span>Ejemplo: sucesión de Fibonacci</a></span></li><li><span><a href="#Resumen" data-toc-modified-id="Resumen-2.4"><span class="toc-item-num">2.4&nbsp;&nbsp;</span>Resumen</a></span></li></ul></li><li><span><a href="#Memoización" data-toc-modified-id="Memoización-3"><span class="toc-item-num">3&nbsp;&nbsp;</span><em>Memoización</em></a></span><ul class="toc-item"><li><span><a href="#Cachés-y-Memoización" data-toc-modified-id="Cachés-y-Memoización-3.1"><span class="toc-item-num">3.1&nbsp;&nbsp;</span>Cachés y Memoización</a></span></li><li><span><a href="#Resumen" data-toc-modified-id="Resumen-3.2"><span class="toc-item-num">3.2&nbsp;&nbsp;</span>Resumen</a></span></li></ul></li></ul></div>
<!-- #endregion -->

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

### Tipo Range

Veamos el siguiente código:

```python
r = range(2,100,3)
r[10]
```

Normalmente, se usa la función `range` para crear bucles sin tener en cuenta que
realmente es un constructor de objetos de tipo `Range`. Estos objetos responden
a los mismos métodos que una lista, permitiendo obtener un elemento de cualquier
posición de la secuencia sin necesidad de generar la secuencia completa. También
se pueden hacer otras operaciones habituales con listas:

```python
# obtener el tamaño
len(r)
```

```python
# obtener un rango
r[20:30]
```

```python
# obtener un rango inverso
r[30:20:-1]
```

```python
# la misma secuencia invertida
r[::-1]
```

```python
# umm, secuencia vacía???
r[20:30:-1]
```

```python
# una nueva secuencia con distinto paso
r[::2]
```

```python
# comprobar si contiene un elemento
3 in r
```

```python
# buscar la posición de un elemento
r.index(65)
```

Como vemos, de algún modo calcula los nuevos rangos y los pasos según
necesitemos. Es suficientemente inteligente para cambiar el elemento final por
otro que considere más apropiado.

Digamos que un objeto de tipo `Range` conoce cómo operar con secuencias
aritméticas, pudiendo obtener un elemento cualquiera de la secuencia sin tener
que calcular el resto.

### Secuencias con elemento genérico conocido

Probemos a crear algo similar a `Range` para la secuencia de cuadrados. Derivará
de la clase abstracta `Sequence`, por lo que tenemos que definir, por lo menos,
los métodos `__len__` y `_getitem__`. Nos apoyaremos en un objeto _range_ para
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
for i in SquaresRange(-10, 1, 3):
    print(i)
```

```python
list(SquaresRange(-1, 50, 4)[:30:2])
```

```python
SquaresRange(100)[::-1]
```

```python
16 in SquaresRange(-10, 1, 3)
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
for i in SquaresRange(-10, 1, 3):
    print(i)
```

```python
for i in CubicsRange(-10, 1, 3):
    print(i)
```

```python
list(CubicsRange(-1, 50, 4)[:30:2])
```

```python
SquaresRange(100)[::-1]
```

```python
SquaresRange(100).index(81)
```

### Resumen

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

## Secuencias infinitas

### Algunas definiciones

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

[glosario]: https://docs.python.org/3.9/glossary.html

### Secuencias infinitas

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

[itertools]: https://docs.python.org/3.9/library/itertools.html
[itertools-recipes]: https://docs.python.org/3.9/library/itertools.html#itertools-recipes

```python
from itertools import count

ℕ = count(0)
```

Para obtener los primeros 100 números naturales

```python
from itertools import islice

print(list(islice(ℕ, 100)))
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

```python tags=["active-md"]
ℕ = count(0)
cuadrados = (n**2 for n in ℕ)
res = [x for x in cuadrados if 100<=x<200]
```

Si probabos es posible que se quede en un bucle infinito. Necesita comprobar todos los elementos, por lo que se pondrá a calcular todos lo elementos de la sucesión para ver si cumplen la condición.

Como sabemos que la sucesión de cuadrados es creciente, podemos pararla en el momento que se salga de límites:

```python
from itertools import dropwhile, takewhile

ℕ = count(0)
cuadrados = (n ** 2 for n in ℕ)
mayores_100 = dropwhile(lambda x: x < 100, cuadrados)
menores_200 = takewhile(lambda x: x <= 200, mayores_100)
list(menores_200)
```

En definitiva, hemos encadenado varias funciones hasta conseguir el iterador que
necesitábamos. En _programación funcional_, a este encadenado de funciones se
denomina como _composición de funciones_ y es bastante utilizado.
Lamentablemente, en python no existe este tipo de operaciones.

### Ejemplo: sucesión de Fibonacci

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

<!-- #region -->

La lista de los 20 primeros:

```python
[1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765]
```

Un modo simple de construir la serie es usar un generador:

<!-- #endregion -->

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
next(islice(fib(), 1000, None))
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
```

```python
list(FibRange(100,110))
```

Lamentablemente, aunque al final se obtenga un número entero, para hacer el
cálculo hemos recurrido al cálculo numérico de coma flotante, lo que produce
desbordamiento cuando trabajamos con números grandes. Tenemos que buscar otros
métodos para mantenernos en el dominio de los número enteros. Pero lo dejaremos
ya para el próximo artículo, donde veremos las _memoizaciones_ o el modo de
guardar los resultados de un función para evitar repetir el mismo cálculo cuando
se vuelva a necesitar.

### Resumen

Las secuencias numéricas se pueden expresar en forma de _iterables_, de las que
tenemos dos tipos: `iteradores` y `secuencias`.

Normalmente en python, para trabajar con secuencias infinitas se usan
iteradores. Para poder manejar estos iteradores se usan las funciones del módulo
`itertools` que podemos combinar para obtener como resultado un iterable que ya
podemos manejar mejor.

Si la secuencia tiene definido un elemento genérico, entonces podemos utilizar
los rangos que ya habíamos visto anteriormente para crear la secuencia infinita.

## _Memoización_

### Cachés y Memoización

En el pasado artículo vimos que para obtener un elemento de la sucesión
fibonacci necesitábamos calcular los anteriores. Veámoslo con más detalle.

Podemos definir la siguiente función para obtener un elemento de esta sucesión:

```python
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)
```

Esta función tiene un terrible problema de eficacia, puesto que se llama a sí
misma demasiadas veces para calcular el mismo elemento. Por ejemplo, para
calcular `fib(10)` llama una vez a `fib(9)` y a `fib(8)`, pero para calcular
`fib(9)` también llama a `fib(8)`. Si sumamos todas las llamadas, habrá
necesitado llamar:

- `fib(9)` 1 vez
- `fib(8)` 2 veces
- `fib(7)` 3 veces
- `fib(6)` 5 veces
- `fib(5)` 8 veces
- `fib(4)` 13 veces
- `fib(3)` 21 veces
- `fib(2)` 34 veces
- `fib(1)` 55 veces
- `fib(0)` 34 veces

Para elementos mayores, todavía serán más las llamadas que se habrán repetido.

Un mejora nos la da la propia documentación de python como aplicación de la
función [`functools.lru_cache`][1]:

[1]: https://docs.python.org/3.9/library/functools.html#functools.lru_cache

```python
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)
```

Básicamente, `lru_cache` es un _decorador_ que detecta los argumentos que se
pasa a una función y guarda en un caché el resultado que devuelve. Un **caché
LRU** (_Least Recently Used_ ) tiene la estrategia de eliminar de la caché los
elementos que hayan sido menos utilizados recientemente. En este caso, con
`maxsize=None` no se impone ningún límite de tamaño, por lo que guardará todos
los elementos de la caché. (Existe un decorador equivalente, `functools.cache`, que también sirve para
crear cachés sin límite, pero no contabiliza el número de aciertos).

A este proceso de guardar los resultados de una evaluación en función de los
argumentos de entrada se conoce por **"memoize"** o **"memoización"**, y es
fundamental para la _evaluación perezosa_.

Podemos obtener información de la caché:

```python
fib(10)
fib.cache_info()
```

Nos dice que la caché tiene 11 elementos (la serie de `fib(0)` a `fib(10)`), que
ha fallado 11 veces, una por elemento de la sucesión, pero sí que ha acertado 8.
Una importante mejora de como lo teníamos antes.

Aún así, en python tenemos limitado el número de llamadas recursivas que se pueden hacer, que suele estar en torno a unas 3000 llamadas recursivas (El límite de llamadas recursivas se obtiene con la función
`sys.getrecursionlimit()` y se podría alterar con `sys.setrecursionlimit`, aunque no es recomendable):

```python
fib(10000)
```

<!-- #region tags=[] -->

Para no tener este problema, en la documentación hacen el truco de ir visitando
en orden todos los elementos de la sucesión hasta llegar al que queremos.

<!-- #endregion -->

```python
[fib(n) for n in range(16)]
```

Con este truco se instruye a la caché con todos los elementos de la sucesión
hasta llegar al que queremos. Para el cálculo de un elemento sólo
se necesitarán los dos elementos anteriores de la sucesión, que ya tendremos en
la caché, lo que evita múltiples llamadas recursivas.

Con este mismo propósito, podemos probar a calcular el elemento 10000 aplicando
las técnicas ya aprendidas hasta ahora:

```python
from itertools import count, islice
from functools import lru_cache

ℕ = count(0)
suc_fib = (fib(n) for n in ℕ)
fib10k = next(islice(suc_fib, 10000, None))
```

Esta gestión de la caché es totalmente opaca para nosotros. Si pudiéramos
acceder a ella sería un modo de obtener la sucesión de fibonacci hasta el mayor
elemento que se haya calculado.

Vamos a itentar a crear una caché similar capaz de generar automáticamente los
elementos de la sucesión:

```python
def fibcache(f):
    cache = []
    def wrap(n):
        for i in range(len(cache), n + 1):
            cache.append(f(i))
        return cache[n]

    wrap.cache = cache

    return wrap

@fibcache
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)
```

Hemos creado el decorador, `fibcache` que añade una caché a la función que
decora. Al hacer la llamada `fib(n)`, este decorador se asegura que todos los
elementos anteriores de la sucesión estén en la caché. La caché es accesible
mediante el atributo `fib.cache`, que no será otra cosa que la sucesión de
fibonacci.

```python
fib(10000)
```

```python
fib.cache[10000]
```

Lo genial de esta estrategia es que sólo calculamos los mínimos elementos
necesarios para obtener el resultado buscado, algo que es el fundamento de lo
que conocemos por _evaluación perezosa_.

### Resumen

Aplicando técnicas de _memoización_, hemos conseguido que una función recursiva
almacene los cálculos que hace para así evitar repetirlos, con lo que es posible
reducir los niveles de recursividad.

Con un decorador, hemos asociado una caché a una función que se rellena
automáticamente, y en orden, con los resultados intermedios hasta llegar al
resultado solicitado. Esta caché será una sucesión ordenada de resultados, que
crece a medida que se necesite.

A este proceso de realizar cálculos según sea necesario es lo que conocemos por
_Evaluación Perezosa_.
