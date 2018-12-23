---
Title: Los iteradores parecen listas, pero no lo son
Date: 2016-01-18 19:55:48.102280
Modified: 2018-07-25 20:45:26
Author: Chema Cortés
Category: Python
Tags: tips, iteradores
Slug: los-iteradores-parecen-listas-pero-no-lo-son
Status: draft
Summary: En python existe cierta dualidad entre listas e iteradores. Bastantes de los métodos de la librería estándar que utilizan listas también suelen aceptar iteradores, no siendo necesario convertir previamente el iterador en lista para invocarlos. Incluso es posible sustituir el argumento por una expresión generadora contruida a propósito para la llamada. ¿Es posible usar estos iteradores sin necesidad de convertirlos en listas?
---

En python existe cierta dualidad entre listas e iteradores. Bastantes métodos de la librería estándar que utilizan listas también suelen aceptar iteradores, no siendo necesario convertir previamente el iterador en lista para invocarlos. Es incluso posible sustituir la lista por una expresión generadora contruida a propósito para la llamada.

Por ejemplo, imagina que necesitamos saber cuál es la mayor longitud de línea que tenemos en un fichero:

~~~ python
with open("fichero.txt") as f:
    maxlen = max(len(line) for line in f)
    print("Longitud mayor:", maxlen)
~~~

No ha hecho falta leer todo el fichero en memoria, ni crear una lista con las longitudes de cada línea. La función `max` ha sido capaz de operar con la expresión generadora para calcular el máximo valor de línea resultante. La principal ventaja es que no malgastamos recursos de memoria ya que el generador ha leído el fichero línea a línea, según ha ido necesitando.

Imagina ahora que necesitamos saber la longitud media de línea que tiene un fichero. Podemos aprovechar el módulo `statistics` y hacer algo parecido:

~~~ python
from statistics import mean

with open("fichero.txt") as f:
    meanlen = mean(len(line) for line in f)
    print("Longitud media:", meanlen)
~~~

El problema de los iteradores es que se "agotan". Si quisiéramos volverlos a usarlos, tendríamos que recrearlos de nuevo tantas veces como cálculos hiciéramos. En el ejemplo que estamos viendo, necesitaríamos volver a leer el fichero, lo que no es un uso eficiente de recursos.

Una técnica que podemos aplicar es una similar a las que vimos en un anterior [artículo sobre clausuras][1]. Consiste en crear una clase que se encargue de realizar los cálculos en cada iteración:

~~~ python
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
~~~

Es un código muy mejorable, pero sirve para ilustrar las posibilidades que existen. En general, es posible operar con un iterador empleando métodos similares a los usados con listas. No es algo intituitivo en algunos casos, como veremos a continuación.

En la documentación del módulo `itertools` se ven algunas recetas interesantes:

## Obtener un elemento arbitrario

...

## consumir un iterador

...

## conversión

...

## split (tee)

...

[1]: {filename}/viejoblog/clausuras-en-python-parte-2.md "Clausuras en python - Parte 2"
