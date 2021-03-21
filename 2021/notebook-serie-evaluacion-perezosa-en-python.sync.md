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
    toc_cell: false
    toc_position:
      height: calc(100% - 180px)
      left: 10px
      top: 150px
      width: 336px
    toc_section_display: true
    toc_window_display: true
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
len(r)  # obtener el tamaño
```

```python
r[20:30]  # obtener un rango
```

```python
r[30:20:-1]  # obtener un rango inverso
```

```python
r[::-1]  # la misma secuencia invertida
```

```python
r[20:30:-1]  # umm, secuencia vacía???
```

```python
r[::2]  # una nueva secuencia con distinto paso
```

```python
3 in r  # comprobar si contiene un elemento
```

```python
r.index(65)  # buscar la posición de un elemento
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

Siguiendo más allá, podemos generalizar esta secuencia para usar cualquier
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
[glosario](https://docs.python.org/3.9/glossary.html) de python):

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
Necesitamos las funciones del módulo [itertools](https://docs.python.org/3.9/library/itertools.html) capaces de operar con
iteradores para pasar a una lista en el momento que realmente la necesitemos. Al
final de la documentación del módulo se incluyen algunas
[recetas](https://docs.python.org/3.9/library/itertools.html#itertools-recipes) que dan idea de lo que pueden hacer.

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

### Ejemplo: sucesión de Fibonacci

La sucesión de _Fibonacci_ se define de la siguiente manera:

$$\begin{align*}
f_0 &= 1 \\
f_1 &= 1 \\
f_n &= f_{n-1} + f_{n-2}
\end{align*}
$$

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

```
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
`itertools` que podemos combinar para obtener como resultado un iterable  que ya
podemos manejar mejor.

Si la secuencia tiene definido un elemento genérico, entonces podemos utilizar
los rangos que ya habíamos visto anteriormente para crear la secuencia infinita.

## Memoización

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
los elementos de la caché. (Existe un decorador equivalente, functools.cache, que también sirve para crear cachés sin límite, pero no contabiliza el número de aciertos).

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

Aún así, en python tenemos limitado el número de llamadas recursivas que se
pueden hacer, que suele estar en torno a unas 3000 llamadas recursivas. (El límite de llamadas recursivas se obtiene con la función`sys.getrecursionlimit()` y se podría alterar con `sys.setrecursionlimit`,
aunque no es recomendable):

```python
fib(10000)
```

Para no tener este problema, en la documentación hacen el truco de ir visitando
en orden todos los elementos de la sucesión hasta llegar al que queremos.

```python
[fib(n) for n in range(16)]
```

Con este truco se instruye a la caché con todos los elementos de la sucesión
hasta llegar al que queremos. Para el cálculo de un elemento sólo se necesitarán
los dos elementos anteriores de la sucesión, que ya tendremos en la caché, lo
que evita múltiples llamadas recursivas.

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

Vamos a itentar crear una caché similar capaz de generar automáticamente los
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

### Calculo de números primos

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

### Secuencia de números primos

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
print(primes[:100])
```

```python
primes[90000]
```

```python
isprime(2**31-1)
```

```python
(2**31-1) in primes._primes
```

```python
primes.last
```

Para cumplir con el protocolo `Sequence` podemos añadir los métodos que nos
faltan, cosa que animo hacer al lector. El método `count()` es trivial: si es
primo, habrá 1 ocurrencia; si no es primo, 0 ocurrencias. El método `index()` es
algo más complicado. En cambio el `_reversed__()` es imposible ya que no se
puede invertir una secuencia infinta. A pesar de ello, la clase `Prime` se
comportará casi como una secuencia siempre y cuando no itentemos acceder a la
secuencia por el final.

### Más optimizaciones

#### Bisecciones

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

#### Programación dinámica

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

#### Multiproceso

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

#### Código final optimizado

El código final optimizado, sin usar concurrencia, se puede encontrar al final del notebook: [primes.py](#Primes)

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

## Formalización de la Secuencia Perezosa

Hasta ahora hemos visto cómo crear una _secuencia perezosa_ que va guardando en
una caché los resultados de una operación (proceso de _memoización_). Así mismo,
cuando la secuencia es una _secuencia ordenada_ podemos optimizar algunas
búsquedas, tal como vimos con la secuencia de números primos.

Vamos a intentar darle una forma a todo esto creando las clases `LazySequence` y
`LazySortedSequence`.

El código refactorizado final se encuentra al final del notebook: [lazyseq.py](#LazySequence-y-LazySortedSequence)

### LazySequence

La clase `LazySequence` crea una _secuencia perezosa_ a partir de un iterador.
A medida que obtenga elementos del iterador, los va almacenando en una caché:

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

Y añadimos el método `__iter__` para cumplir con el protocolo _iterator_:

```python
    def __iter__(self) -> Iterator[T]:
        yield from self._cache
        yield from (self[i] for i in range(len(self._cache), INFINITE))
```

### LazySortedSequence

Derivando de `LazySequence`, se crea la clase `LazySortedSequence` para cuando
el iterador produzca una secuencia ordenada. Tal como hemos visto, cuando la
secuencia está ordenada podemos realizar búsquedas por _bisecciones_ que
resultan bastante eficiente.

La operación principal será el método `insertpos()` que nos indica la posición
en la que se insertaría un elemento en la secuencia, manteniendo el orden de los
elementos. Si no son suficientes con los elementos de la caché, se extraerán más
del iterador mediante `next()`, que irán añadiéndose progresivamente a la caché:

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

Con el método `insertpos()` ya podemos definir los métodos `__contains__()` e
`index()` típicos de la secuencias:

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

No existe un protocolo para elementos _ordenables_ (`Sortable`, `Ordered`). Para
ordenar elementos se usan los métodos de comparación `__eq__`, `__ne__`,
`__lt__`, `__le__`, `__gt__` y `__ge__`. Pero se suele considerar estos métodos
redundantes ya que basta con definir sólo dos (eg: `__eq__` y `__lt__`) para
establecer una ordenación.

Como no hay una forma mejor, hemos creado el tipo genérico `Ord` enlazado con
`int` para que al menos el chequeador de tipos no se queje en la comparaciónes,
aunque no tiene porqué limitarse su aplicación a números enteros.

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

Si dejamos así la codificación, la clase `Primes` usará el método `__contains__`
de `LazySortedSequence`. Este método añadirá primos a la caché hasta alcanzar el
argumento solicitado.

Si recordamos de la implementación anterior que teníamos de la clase `Primes`,
el método `__contains__()` estaba optimizado para comprobar la pertencia de un
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

[genericrange.py]: {attach}/code/2021Q1/lazyseq/genericrange.py "GenericRange class"
[lazyseq.py]: {attach}/code/2021Q1/lazyseq/lazyseq.py "LazySequence class"
[primes.py]: {attach}/code/2021Q1/lazyseq/primes.py "Primes class"

## Ejemplo práctico: potencias de Fermi-Dirac

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

### Estudio previo

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
potencias = sorted(p**2**k for p in primes[:14] for k in range(0, 14))
print(potencias[:14])
```

Aún en el caso de que tuviéramos algún medio de reducir el número de elementos a
usar de cada secuencia, seguimos sin saber cuántos números primos serán
necesarios. Para sacar los 14 primeros elementos de las potencias de Fermi-Dirac
sólo se necesitaban los 10 primeros números primos.

Es evidente que una estrategia por _fuerza bruta_ es complicada y termina por
hacer muchos cálculos innecesarios, una complejidad del $O({n^2})$ no resoluble
con un ordenador normal. Veamos cómo nos puede ayudar la _evaluación perezosa_.

### Modelos

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
este límite en las pruebas. (Es posible que en posteriores artículos veamos técnicas para superar las limitaciones de la recursivad en python).

### código final

Se puede ver el código al final del notebook: [potencias.py](#Potencias-de-Fermi-Dirac)


Para las comprobaciones:

```python
potencias[:14]
```

```python
potencias[60]
```

```python
potencias[10 ** 6]
```

```python
primes.size
```

Para obtener el elemento $10^6$ tarda bastante al necesitar obtener casi un
millón de números primos. Una vez obtenidos, el cálculo es bastante rápido.

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

### Secuencia de enteros

He empleado el tipo `Sequence` sin indicar de qué tipo son los elementos. Un
chequeador de tipos asume que se trata de un iterable de elementos de tipo
`Any`, por lo que no debería dar problemas. Pero siempre podemos ser más
precisos y usar `Sequence[int]` como tipo de datos para nuestras secuencias de
números enteros.

### Referencia _forward_

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

### Unión de tipos

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

### Código final

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

### Conclusión

Python está realizando un gran esfuerzo en incorporar _anotaciones de tipo_ sin
perder con ello sus característicos tipos _ducking_. De igual modo, vamos a ver
cómo se incorporan más elementos de otros lenguajes como las _dataclasses_,
_programación asíncrona_ o los _patrones estructurales_, aunque tardarán en ser
adoptados por la mayor parte de programadores python.

Si algo tiene python es no tener demasiada prisa en que se apliquen sus cambios.
Como decía un gran sabio: _"Vamos a cambiarlo todo para que todo siga igual"_.

<!-- #region -->
## Códigos finales

### GenericRange
<!-- #endregion -->

```python
from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence
from functools import singledispatchmethod


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
    def from_range(cls: type[GenericRange], rng: range) -> GenericRange:
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
def __(self, idx: slice) -> GenericRange:
    i = self._range[idx]
    return self.from_range(i)

```

### LazySequence y LazySortedSequence


Secuencias perezosas creadas a partir de un iterador

- `LazySequence`: secuencia que cachea los elementos obtenidos de un iterador
- `LazySortedSequence`: secuencia perezosa de elementos ordenados

```python
import sys
from bisect import bisect_left
from collections.abc import Iterator
from functools import singledispatchmethod
from itertools import islice
from typing import Optional, TypeVar

INFINITE = sys.maxsize  # una mala aproximación de infinito

# Generic Types
T = TypeVar("T", covariant=True)
Ord = TypeVar("Ord", bound=int, covariant=True)


class LazySequence(Iterator[T]):
    """
    Secuencia perezosa creada a partir de un iterador
    """

    def __init__(self, iterator: Iterator[T]):
        self._cache: list[T] = []
        self.iterator = iterator

    @property
    def last(self) -> Optional[T]:
        return self._cache[-1] if self.size > 0 else None

    @property
    def size(self) -> int:
        return len(self._cache)

    def __next__(self) -> T:
        x = next(self.iterator)
        self._cache.append(x)
        return x

    def __iter__(self) -> Iterator[T]:
        yield from self._cache
        yield from (self[i] for i in range(len(self._cache), INFINITE))

    def islice(self, start, stop=-1, step=1) -> Iterator[T]:
        if stop == -1:
            start, stop = 0, start
        if stop is None:
            stop = INFINITE
        yield from (self[i] for i in range(start, stop, step))

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


class LazySortedSequence(LazySequence[Ord]):
    """
    Secuencia perezosa ordenada creada a partir de un iterador
    """

    def insertpos(self, x: int) -> int:
        """
        Posición donde insertar un elemento para mantener la lista ordenada
        Obtiene los elementos necesarios hasta llegar a la posición
        """
        if self.size > 0 and x <= self.last:
            idx = bisect_left(self._cache, x)
        else:
            while x > next(self):
                pass
            idx = self.size - 1

        return idx

    def __contains__(self, x: int) -> bool:
        idx = self.insertpos(x)
        return x == self._cache[idx]

    def index(self, x: int) -> int:
        idx = self.insertpos(x)
        if x == self._cache[idx]:
            return idx
        raise ValueError(f"{x} is not in {self.__class__.__name__}")

```

### Primes

```python
from collections.abc import Iterator
from itertools import islice
from math import isqrt
from typing import final


Prime = int


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


primes = Primes()
isprime = primes.__contains__

```

### Potencias de Fermi-Dirac


Se llaman **potencias de Fermi-Dirac** a los números de la forma $p^{2^k}$,
donde p es un número primo y k es un número natural.

Definir la sucesión

```haskell
potencias :: [Integer]
```

cuyos términos sean las potencias de Fermi-Dirac ordenadas de menor a mayor. Por
ejemplo,

```haskell
take 14 potencias    ==  [2,3,4,5,7,9,11,13,16,17,19,23,25,29]
potencias !! 60      ==  241
potencias !! (10^6)  ==  15476303
```

```python
from collections.abc import Iterator
from itertools import count
from typing import TypeVar

# Se vincula al tipo int, ya que no existe protocolo Ordered o Sortable
Ord = TypeVar("Ord", bound=int)

SortedIterator = Iterator[Ord]


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
