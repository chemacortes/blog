Title: Mutabilidad de Listas
Date: 2013-03-16 15:53
Modified: 2018-07-25 01:15:35
Author: Chema Cortés
Category: Python
Slug: mutabilidad-de-listas

!!! INFO
    Puedes visionar este artículo y descargártelo como notebook ipython en [http://nbviewer.jupyter.org/5177340](http://nbviewer.jupyter.org/5177340)

Mucha gente, cuando se enfrenta por primera vez al lenguaje python, no entiende bien el concepto de *"inmutabilidad"* que tanto repite la documentación al tratar de diferenciar algunos tipos contenedores como tuplas, listas, conjuntos y diccionarios.

Por lo general, la gente formada en lenguajes de programación clásicos tiene la idea de que las variables son porciones de memoria donde colocar valores. Que una variable no se éso, *variable*, resulta un contrasentido. Han visto *constantes*, pero sólo sirven para inicializar variables y poco más. Si en su carrera hubieran sido formados en algún lenguaje funcional se darían cuenta que hay quienes piensan que las variables que cambian de valor son las raras, que lo más natural es que una variable conserve su valor inicial, o sea, que sea inmutable.

Por poner un ejemplo, el siguiente código está basado en una pregunta reciente en la lista [python-es][1]. Tenemos una lista de pares y queremos quitar las parejas repetidas con orden cambiado:

~~~python
def quitar_dup(lista):

    for item in lista:

        item.reverse()

        if item in lista:
            lista.remove(item)

    return lista

L=[[1, 2], [1, 3], [2, 1], [3, 1]]

print quitar_dup(L)  #res: [[1, 3], [3, 1]]
~~~

A simple vista, el código parece correcto, pero tenemos dos operaciones que pueden mutar listas: `.reverse()` y `.remove()`. De hecho, el resultado es incorrecto: `[[1, 3], [3, 1]]`

A medida que recorremos la lista en el bucle `for`, la lista se va modificando, lo que da lugar a resultados inesperados. Si no lo ves bien, basta añadir algunos `prints` en lugares estratégicos para que comprobar lo que pasa. De hecho, sólo existen dos iteraciones para cuatro elementos que tiene la lista.

Otro tipo de casos son cuando pasamos listas a funciones:

~~~python
>>> def add(a, l):
...   if a not in l:
...     l += [a]
...   return l
...
>>> L = [1, 2, 3]
>>> add(1, L)
[1, 2, 3]
>>> add(4, L)
[1, 2, 3, 4]
>>> L
[1, 2, 3, 4]
~~~

Como efecto colateral, la función ha modificado la lista pasada como argumento, algo que no es siempre deseable. El problema se agrava más si empleamos listas en valores por defecto:

~~~python
>>> def add(a, l=[]):
...   if a not in l:
...     l += [a]
...   return l
...
>>> add(1)
[1]
>>> add(2)
[1, 2]
>>> add(3, [])
[3]
>>> add(4)
[1, 2, 4]
~~~

Como se puede ver, aunque intentemos *resetear* el valor por defecto, la función tiene un efecto memoria que es imposible de eliminar. Este efecto es a veces buscado, pero en general debe ser siempre evitado ya que desvirtúa el sentido que tiene dar valores por defecto.

Estos efectos son todavía más perniciosos con la *funciones lambda*. Al carecer de una *clausura* como las funciones, la evaluación de una función lambda depende del *scope* donde han sido definidas. Por ejemplo, observa esta creación de una lista de funciones:

~~~python
fns = []

for i in range(5):
    fns.append( lambda x: x + i)

print fns[1](10)
print fns[2](10)
~~~

Siempre añade `4` al argumento, que es el valor de `i` al acabar el bucle, independientemente de qué valor tenía esta variable en el momento de crear la función lambda. No es de extrañar que se recomiende dejar de usar estas funciones.

Por último, otro efecto funesto de la mutabilidad de las listas aparece en la creación de *listas multidimensionales* (aka *matrices*). Una forma rápida de crear una matriz de 2x2 es: `[[0]*2]*2`. El problema aquí está en que cuando clonamos listas, en lugar de copiar los elementos, los enlaza entre sí. Quizás se vea mejor si hacemos alguna operación:

~~~plain
>>> l = [[0]*2]*2
[[0, 0], [0, 0]]
>>> l[0][0]
0
>>> l[0][0] = 1
>>> l
[[1, 0], [1, 0]]
>>> l[0] is l[1]
True
~~~

Los elementos `l[0]` y `l[1]` son el mismo elemento. Que los elementos de una lista puedan estar *entrelazados* resulta muy interante para algunos algoritmos de búsquedas. Pero hay que conocer bien lo que estamos haciendo si no queremos llevarnos alguna sorpresa.

## Recomendaciones para hacer código funcional

### Copia de listas

En funciones y métodos, si recibimos una lista como argumento, la primera acción defensiva que deberíamos hacer es copiar la lista en una variable local y trabajar solo con la variable local desde ese momento. Con una asignación directa no se realiza una copia, más bien estaríamos *enlazando* una nueva referenciasin solucionar nada.

La forma consensuada entre programadores python de copiar una lista es con la operación de *spliting* `L[:]`, aunque sirven otras operaciones idempotentes como `L*1` ó `L+[]`[^1]. Para listas de elementos entrelazados tendremos que acudir a otros mecanismos de copia como los que ofrece el [módulo `copy`][1], aunque no será frecuente que lo necesitemos.

~~~python
def add(a, lista):
  l = lista[:]
  if a not in l:
    l += [a]
  return l
~~~

En cuanto a los argumentos por defecto, lo mejor es no usar nunca una lista para tal cosa. Una buena estrategia defensiva consiste en usar `None` de esta forma:

~~~python
def add(a, lista=None):
  l = [] if lista is None else lista[:]
  if a not in l:
    l += [a]
  return l
~~~

### Operaciones inmutables con listas

En cuanto a evitar las operaciones que mutan listas, siempre hay alternativas inmutables de todas estas operaciones. El siguiente cuadro puede servir como referencia:

Mutable      | Inmutable
---- | ----
`L.append(item)` | `L+[item]`
`L.extend(sequence)` | `L + list(sequence)`
`L.insert(index, item)` | `L[:index] + [item] + L[index:]`
`L.reverse()` | `L[::-1]`
`L.sort()` | `sorted(L)`
`item = L.pop()` | `item,L = L[-1],L[:-1]`
`item = L.pop(0)` | `item,L = L[0],L[1:]`
`item = L.pop(index)` | `item, L = L[item], L[:item]+L[item+1:]`
`L.remove(item)` | `L=L[:item]+L[item+1:]`
`L[i:j] = K` | `L[:i] + K + L[j:]`

A la hora de decidir qué versión usar, la versión inmutable es más apropiada para programación funcional y resulta incluos más intuitiva de interpretar. No es extraño ver errores de código donde se espera resultados de las operaciones `.sort()` o `.reverse()`, que siempre devuelven `None`. Para el intérprete de python no hay error, pero a veces nos será difícil darnos cuenta de estos errores:

*MODO ERRÓNEO: machacamos la lista con None*

~~~python
>>> l = [3, 5, 1, 2, 4]
>>> l_2 = [x*x for x in l.sort()]
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: 'NoneType' object is not iterable
~~~

*MODO CORRECTO*

~~~python
>>> l = [3, 5, 1, 2, 4]
>>> l_2 = [x*x for x in sorted(l)]
>>> l_2
[1, 4, 9, 16, 25]
~~~

[^1]: De hecho, la operación `L*1` es más eficiente que `L[:]`.

[1]: http://docs.python.org/3.3/library/copy.html "Módulo copy"
