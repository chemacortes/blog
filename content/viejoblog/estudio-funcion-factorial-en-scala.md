Title: Estudio función factorial en scala
Date: 2011-10-17 20:49
Author: Chema Cortés
Category: Scala
Tags: algorithm, factorial
Slug: estudio-funcion-factorial-en-scala

Como continuación al artículo que dediqué al [estudio del factorial][1], voy a explicar cómo se haría este famoso algoritmo usando [scala][2]. Tengo que añadir que tan sólo llevo una semana con el lenguaje scala, por lo que es muy probable que haya algún aspecto de este lenguaje que me haya dejado por el camino.

## Versión recursiva (y *one-line*)

La forma básica de la función sería:

```scala
def fact(n:Int):BigInt =
    if (n==0) 1
    else n*fact(n-1)
```

Si se compara con la función recursiva en python, no parece que haya mucha diferencia, con excepción de que en scala existe el tipado de datos.

Esta función es en realidad una sóla línea, por lo que podíamos haberla escrito de esta manera:

```scala
def fact(n:Int):BigInt = if (n==0) 1 else n*fact(n-1)
```

Es una clara señal de la orientación funcional que tiene scala.

Al igual que python, esta función recursiva se corta cuando se sobrepasa un cierto límite de llamadas recursivas para proteger la memoria del sistema.

El compilador de Scala posee una optimización especial denominda de *"LLamada Terminal"* ([Tail Call][3])[^1] (optimización que no existe en JVM). Este tipo de optimizaciones son posibles cuando la última línea a ejecutar de la función es únicamente la llamada recursiva a sí misma, con lo cuál hace innecesario guardar el stack de ejecución puesto que no quedarían más líneas para ejecutar.

Para que sea posible aplicar esta optimización de "llamada terminal", tenemos que reescribir nuestra función de modo que la última línea sea una llamada a sí misma. Para ello usaremos una función acumuladora que se encargue de realizar la multiplicación previamente a la llamada. Casi mejor si vemos el código:

```scala
def fact(n:Int):BigInt = {
	def factAcc(n:Int, acc:BigInt):BigInt =
		if (n<=1) acc else factAcc(n-1, n*acc)

	factAcc(n,1)
}
```

En las últimas versiones de scala existe una *"anotación"* especial para indicar al compilador de scala que intente aplicar la optimización de "LLamada Terminal", o que nos dé un aviso de no poder hacerlo. Finalmente, así quedaría el código de nuestra función recursiva:

```scala
import scala.annotation.tailrec

def fact(n:Int):BigInt = {
	@tailrec
	def factAcc(n:Int, acc:BigInt):BigInt=
		if (n<=1) acc else factAcc(n-1, n*acc)

	factAcc(n,1)
}
```

##Versión iterativa

Es la versión más sencilla:

```scala
def fact(n:Int):BigInt = {
    var res=BigInt(1)
    for (i <- 1 to n)
        res*=i
    res
}
```


## Fórmula de Stirling

Para completar el estudio, podemos ver cómo sería la función de Stiling en Scala, bastante similar, como puede verse, a su versión en python:

```scala
import math._

def fact(n:Int):Double =
    sqrt(2*Pi*n)*pow(n/E,n)
```


[1]: {filename}estudio-funcion-factorial.md
[2]: http://scala-lang.org "Scala programming language"
[3]: http://en.wikipedia.org/wiki/Tail_call "Tail Call"
[4]: http://neopythonic.blogspot.com/2009/04/tail-recursion-elimination.html

[^1]: Existe algún intento para implementar esta optimización de "Tail Call" en python, con algunos decoradores más o menos funcionales. Si quieres ver motivos en contra, visita el artículo que escribió Guido sobre el tema: [http://neopythonic.blogspot.com/2009/04/tail-recursion-elimination.html][4]
