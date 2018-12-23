Title: Estudio función factorial - numpy
Date: 2013-08-14 14:28
Author: Chema Cortés
Category: Python
Tags: algorithm, factorial, maths
Slug: estudio-funcion-factorial-numpy

Mientras busco tiempo para preparar algunos artículos sobre cómo hacer la programación python *más eficiente*, he estado revisando nuevos métodos de programar la función factorial en python aplicando los nuevos conocimientos adquiridos.

Como puse en un [artículo anterior][1], la implementación más compacta de la función factorial sería aplicando la función `reduce`:

```python
def fact(n):
    return reduce(lambda x,y:x*y, xrange(2,n+1), 1)
```

...o usando el `operator.__mul__`:

```python
from operator import __mul__

def fact(n):
    return reduce(__mul__, xrange(2,n+1), 1)
```

También contaba el caso de una compresión de listas *"bizarra"* que evitaba el uso de `reduce` y `lambda`:

```python
def fact(n):
    return [j for j in [1] for i in xrange(2,n+1) for j in [j*i]][-1]
```

El problema con esta expresión es que calcula todos los elementos de la lista para quedarse únicamente con el último elemento. Una forma de hacer lo mismo, sabiendo que la función factorial es estrictamente creciente, es obteniendo el máximo con `max`:

```python
def fact(n):
    return max(j for j in [1] for i in xrange(2,n+1) for j in [j*i])
```

Para este tipo de tareas, en las que tenemos un iterador y queremos quedarnos con el último elemento, resulta mucho más eficiente el uso de la colección `deque` limitando el número de elementos de la lista:

```python
from collections import deque

def fact(n):
    return deque((j for j in [1] for i in xrange(2,n+1) for j in [j*i]), maxlen=1)[0]
```

Por comparar tiempos, para el cómputo de `fact(10000)` me salen estos tiempos:

```
reduce+lambda        72.0 ms
reduce+operator      71.2 ms
comprensión listas  173.0 ms
función max          75.1 ms
deque                75.5 ms
```

Como se puede apreciar que los tiempos son muy similares (con la excepción de la compresión de listas debido a su gasto de memoria). Es lógico suponer que donde más tiempo se gasta es el cómputo de la multiplicación con la precisión absoluta que tienen los números *longs* de python. 

De hecho, no se consigue gran cosa usando las librerías de cálculo numérico más conocidas de python. Se hace imposible optimizar nada sin pérdida de precisión o que salgan resultados extraños. Aún así, podemos expresar formas muy compactas para expresar la función factorial en `numpy` si forzamos en el uso del tipo `object` para que así no lo optimice:

```python
import numpy as np

def fact(n):
    return np.arange(2,n+1,dtype=object).prod()
```

Tarda `70.8 ms.` en calcular `fact(10000)`, que es similar al resto de funciones factoriales que hemos visto. Da una buena idea de lo bien optimizada que está la librería `numpy` para cualquier cosa, incluso impidiéndole que optimice los tipos de datos que emplea.



[1]: {filename}estudio-funcion-factorial.md
