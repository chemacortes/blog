---
Title: Clausuras en python - Parte 2
Date: 2013-10-26 04:15
Modified: 2021-01-10 20:03:45
Author: Chema Cortés
Category: Python
Tags: closures
Slug: clausuras-en-python-parte-2
---

## Ámbitos anidados

La importancia de disponer de _clausuras_ va más allá de saber dónde se evalúa
la función. Si fuera posible encapsular una función junto con su propio entorno
de ejecución, podríamos conseguir que la función tenga _"memoria"_ o, dicho de
otro modo, que sea capaz de conservar sus propios estados entre llamadas a la
función. Este _empaquetado_ de función y entorno de ejecución se denomina a
veces **clausuras verdaderas** y suele ser la principal característica de los
llamados _Lenguajes Funcionales_.

En python podemos crear estas _clausuras verdaderas_ con \*_funciones anidadas_,
donde una función está definida dentro del ámbito de la otra.

Un ejemplo sencillo:

```python
def incr(n):
    def aux(x):
        return x + n

    return aux


inc5 = incr(5)

print(inc5(10))  # -->15
```

Como resultado se devuelve la función `aux`, definida dentro del ámbito de
`incr` y que emplea de éste la variable `n`. Internamente, se conserva la
referencia a la variable `n`, pero no será accesible desde fuera de la función
`aux`. Hemos podido empaquetar la función junto con el entorno donde se definió.

Pongamos otro ejemplo:

```python
def count():
    num = 0

    def aux():
        num += 1
        return num

    return aux


c1 = count()

c1()  # --> 1
c1()  # --> 2
c1()  # --> 3
```

Si pruebas este código te dará error. La función anidada `aux` intenta modificar
la variable `num`. Para este caso, la variable se crea dentro del ámbito más
interno, en lugar de usar la variable disponible. Y como se intenta modificar la
variable antes de asignarle un valor, entonces se produce el error.

Como solución, podríamos hacer la variable `num` global para que fuera accesible
por todos los ámbitos. Pero esta solución no es buena ya que nos abriría el
empaquetado. Para python3 podríamos declarar la variable como `nonlocal` para
que se busque en los ámbitos superiores:

```python
def count():
    num = 0

    def aux():
        nonlocal num
        num += 1
        return num

    return aux
```

Como solución para salir del paso, se puede evitar la reasignación de variables.
Por ejemplo, usando una lista:

```python
def count():
    num = [0]

    def aux():
        num[0] += 1
        return num[0]

    return aux
```

Ya sé que no es muy elegante, pero hay otras formas de hacerlo mejor.

## Generadores

Una de las formas más comunes de usar clausuras es a través de **generadores**.
Básicamente, son funciones que en lugar de usar `return` utilizan `yield` para
devolver un valor. Entre invocaciones, se conserva el entorno de ejecución y
continúan desde el punto desde donde estaba. Para el ejemplo anterior:

```python
def count():
    num = 0
    while True:
        num += 1
        yield num


c1 = count()
next(c1)  # --> 1
next(c1)  # --> 2
```

## Objetos funciones

En los ejemplos que hemos visto, podríamos tener varias clausuras de una misma
función. Si hemos hecho bien las tareas, la ejecución de estas clausuras son
independientes:

```python
c1 = count()
c2 = count()

next(c1)  # -->1
next(c1)  # -->2
next(c2)  # -->1
next(c2)  # -->2
next(c1)  # -->3
```

Con ello es posible establecer una analogía con clases y objetos. La definición
de la función sería la _clase_ y la clausura la _instancia_ de la clase.

¿Y si lo hacemos posible? En python se denominan _callables_ a todo objeto que
tenga un método `__call__`, comportándose como si fueran funciones
(_Functores_). Contruyamos una _callable_ que funcione como una función con
clausura:

```python
class Count(object):
    def __init__(self):
        self.num = 0

    def __call__(self):
        self.num += 1
        return self.num


c1 = Count()
c1()  # -->1
c1()  # -->2
c1()  # -->3
```

Sin duda es la manera más elegante de usar clausuras que tenemos en python.
Evita muchos problemas y nos da una gran potencia a la hora de resolver algunos
problemas.

Por ejemplo: imagina que queremos recorrer una lista de números, excluyendo los
que sean pares, y siempre que la suma total de los números que ya hemos visitado
no supere cierto límite.

En una primera aproximación se podría crear un generador:

```python
def recorr(lista, maximo):
    total = 0
    for i in lista:
        if i % 2 != 0:
            if total + i < maximo:
                total += i
                yield i
            else:
                break


recorr([3, 6, 7, 8, 11, 23], 30) #-->[3,7,11]

```

Está bien, pero no es fácil de usar. Aunque sólo necesitemos algunos elementos,
seguramente estemos obligados a crear una lista completa con todos los
valores[^1]. Encima, no tenemos acceso a la variable `total` para saber cuánto
han sumado el resultado.

Una alternativa con objetos funciones, mucho más elegante:

```python
class RecorrFunc(object):
    def __init__(self, maximo):
        self.maximo = maximo
        self.total = 0

    def filter(self, item):
        res = item % 2 != 0 and self.total + item < self.maximo
        if res:
            self.total += item
        return res

    def __call__(self, lista):
        return [x for x in lista if self.filter(x)]


recorr = RecorrFunc(30)
recorr([3, 6, 7, 8, 11, 23])  # -->[3,7,11]
print(recorr.total)  # -->21

```

Las posibilidades de los objetos función son muchas. Del mismo modo que se
devuelve una lista, sería posible devolver un iterador. Empleando las funciones
del módulo `itertools`, y algunos trucos más, podríamos aplicar los principios
de la programación funcional en python sin problemas.

Pero éso lo veremos en próximos artículos.

[^1]: No sabemos de antemano cuántos items vamos a obtener. Si, por ejemplo,
    necesitamos sólo los tres primeros, tendremos que iterar elemento a elemento
    hasta llegar a los tres que necesitamos o, bien, hasta que quede exhausto el
    iterador. Con la solución con funtores el proceso es mucho más directo y
    eficiente.
