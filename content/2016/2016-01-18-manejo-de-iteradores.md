---
Title: Manejo de iteradores
Date: 2016-01-18 19:55:48.102280
Modified: 2022-07-19 21:35:55
Author: Chema Cortés
Category: Python
Tags: tips, iteradores
Slug: manejo-de-iteradores
Status:
Summary: En python existe cierta dualidad entre listas e iteradores. Bastantes de los métodos de la librería estándar que utilizan listas también suelen aceptar iteradores, no siendo necesario convertir previamente el iterador en lista para invocarlos. Incluso es posible sustituir el argumento por una expresión generadora contruida a propósito para la llamada. ¿Es posible usar estos iteradores sin necesidad de convertirlos en listas?
---

!!! note "Artículo viejo"
    Este artículo lo he rescatado de un borrador que tenía desde 2016. Está sin
    terminar, pero creo puede interesar tal como está.

En python existe cierta dualidad entre listas e iteradores. Bastantes métodos de
la librería estándar que utilizan listas también suelen aceptar iteradores, por
lo que no es necesario convertir el iterador en lista para invocar algunas
funciones. Incluso es posible sustituir la lista por una expresión generadora
contruida a propósito para la llamada.

Por ejemplo, imagina que necesitamos saber cuál es la mayor longitud de las
líneas de un fichero:

```python
with open("fichero.txt") as f:
    maxlen = max(len(line) for line in f)
    print("Longitud mayor:", maxlen)
```

Hemos procesado todo el fichero, línea a línea, sin necesidad de leer todo el
fichero completo en memoria, ni crear una lista auxiliar con las longitudes de
cada línea. La función `max` ha sido capaz de operar con la expresión generadora
para calcular el máximo valor de línea resultante. La principal ventaja es que
no malgastamos recursos de memoria ya que el generador ha leído el fichero línea
a línea, según ha ido necesitando.

Imagina ahora que necesitamos saber la longitud media de línea que tiene un
fichero. Podemos aprovechar el módulo `statistics` y hacer algo parecido:

```python
from statistics import mean

with open("fichero.txt") as f:
    meanlen = mean(len(line) for line in f)
    print("Longitud media:", meanlen)
```

El problema de los iteradores es que se _"agotan"_. Si quisiéramos volverlos a
usarlos, tendríamos que recrearlos de nuevo tantas veces como cálculos
hiciéramos. En el ejemplo que estamos viendo, necesitaríamos volver a leer el
fichero, lo que no es un uso eficiente de recursos.

Una técnica que podemos aplicar es una similar a las que vimos en un anterior
[artículo sobre clausuras][1] consistente en crear una clase que se encargue de
realizar los cálculos en cada iteración:

```python
class Calc:
    def __init__(self, iterable):
        self.num = 0
        self.total = 0
        self.maxlen = max(iterable, key=self.iteration)

    @property
    def mean(self):
        return self.total / self.num

    def iteration(self, nlen):
        self.num += 1
        self.total += nlen
        return nlen

with open("fichero.txt") as f:
    calc = Calc(len(line) for line in f)
    print("Longitud mayor:", calc.maxlen)
    print("Longitud media:", calc.mean)
    print("Total líneas:", calc.num)
```

En el parámetro `key` de `max()` hemos pasado el método `Calc.interation()`.
Este método devuelve el mismo valor que se le pasa como argumento (la longitud
de línea), lo único que hace es incrementar el número de líneas y actualizar el
total.

Es un código muy mejorable, pero sirve para ilustrar las posibilidades que
existen. En general, es posible operar con un iterador empleando métodos
similares a los usados con listas.

En la documentación del módulo `itertools` se ven algunas recetas interesantes:


...

[1]: {filename}/viejoblog/clausuras-en-python-parte-2.md "Clausuras en python - Parte 2"
