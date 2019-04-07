---
Title: Factorial en scala en paralelo
Date: 2018-07-25 20:49:57
Modified: 2018-08-14 01:00:09
Category: Scala
Tags: algorithms, factorial
Slug:
Authors: Chema Cortés
Summary: Una nueva versión del factorial en scala, ahora en paralelo
Lang: es
Translation: false
---

Una obsesión de este blog siempre ha sido crear cálculos de la función *factorial* con diversos algoritmos y con cualquier lenguaje.

Para no perder la costumbre, veamos una de las formas más rápidas de calcular un factorial aprovechando las CPUs multicores que equipan los equipos modernos.

Teníamos en scala una definición de este estilo:

~~~ scala
def factorial(n: Int): BigInt = (BigInt(2) to n).product
~~~

El producto de los números se realiza en secuencia, desde el `2` hasta `n`. Como variante podíamos haber recorrido la secuencia en orden inverso:

~~~ scala
def factorial(n: BigInt): BigInt = (n to 2 by -1).product
~~~

Puede pensarse que el orden en el que se multiplican los números podría influir en el tiempo de cómputo, pero las pruebas que he hecho no parece que tenga demasiada influencia. Tal vez resulte ligeramente más costosa en orden inverso.

Una forma simple que tenemos de acelerar el producto sería convertir la secuencia en una *colección paralela*, algo tan sencillo como invocar el método `.par` de la secuencia:

~~~ scala
def factorial(n: Int): BigInt = (BigInt(2) to n).par.product
~~~

Ahora el producto se realiza en paralelo, usando todos los *cores* disponibles de la CPU. Para números pequeños, casi no se nota el incremento de velocidad debido a los cambios de contexto que realiza el cómputo. Pero en números bastantes grandes, la velocidad se multiplica prácticamente por el número de cores disponibles.