---
Title: Memoización - Evaluación perezosa en python - Parte 3
Date: 2021-02-14 17:53:58
Modified: 2021-03-08 00:05:00
Category: Python
Tags: lazy-eval, memoize, cache
Slug: evaluacion-perezosa-en-python-parte-3
Authors: Chema Cortés
Summary: Tercera parte de una serie de artículos dedicados al estudio de la evaluación perezosa en python. En esta parte veremos la técnica de memoización y cómo puede ayudarnos en la implementación de secuencia de evaluaciones.
Lang: es
Translation: false
Status:
---

## Cachés y Memoización

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
los elementos de la caché [^1].

A este proceso de guardar los resultados de una evaluación en función de los
argumentos de entrada se conoce por **"memoize"** o **"memoización"**, y es
fundamental para la _evaluación perezosa_.

Podemos obtener información de la caché:

```python
>>> fib(10)
>>> fib.cache_info()
CacheInfo(hits=8, misses=11, maxsize=None, currsize=11)
```

Nos dice que la caché tiene 11 elementos (la serie de `fib(0)` a `fib(10)`), que
ha fallado 11 veces, una por elemento de la sucesión, pero sí que ha acertado 8.
Una importante mejora de como lo teníamos antes.

Aún así, en python tenemos limitado el número de llamadas recursivas que se
pueden hacer, que suele estar en torno a unas 3000 llamadas recursivas [^2]:

```python
>>> fib(10000)
...
RecursionError: maximum recursion depth exceeded in comparison
```

Para no tener este problema, en la documentación hacen el truco de ir visitando
en orden todos los elementos de la sucesión hasta llegar al que queremos.

```python
>>> [fib(n) for n in range(16)]
[0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
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
>>> fib(10000)
3364476487643178326662161200510754331030214846068006390656476997468008144216....
...
>>> fib.cache[10000]
3364476487643178326662161200510754331030214846068006390656476997468008144216....
...
```

Lo genial de esta estrategia es que sólo calculamos los mínimos elementos
necesarios para obtener el resultado buscado, algo que es el fundamento de lo
que conocemos por _evaluación perezosa_.

## Resumen

Aplicando técnicas de _memoización_, hemos conseguido que una función recursiva
almacene los cálculos que hace para así evitar repetirlos, con lo que es posible
reducir los niveles de recursividad.

Con un decorador, hemos asociado una caché a una función que se rellena
automáticamente, y en orden, con los resultados intermedios hasta llegar al
resultado solicitado. Esta caché será una sucesión ordenada de resultados, que
crece a medida que se necesite.

A este proceso de realizar cálculos según sea necesario es lo que conocemos por
_Evaluación Perezosa_.

-----

{! content/2021/2021-02-08-serie-evaluacion-perezosa-en-python.txt !}

-----

ANOTACIONES:

[^1]: Existe un decorador equivalente, `functools.cache`, que también sirve para
crear cachés sin límite, pero no contabiliza el número de aciertos.

[^2]: El límite de llamadas recursivas se obtiene con la función
`sys.getrecursionlimit()` y se podría alterar con `sys.setrecursionlimit`,
aunque no es recomendable.

[1]: https://docs.python.org/3.9/library/functools.html#functools.lru_cache
