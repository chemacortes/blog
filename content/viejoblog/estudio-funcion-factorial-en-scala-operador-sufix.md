Title: Estudio función factorial en scala - operador sufix
Date: 2012-08-15 09:30
Author: Chema Cortés
Category: Scala
Tags: algorithm, factorial
Slug: estudio-funcion-factorial-en-scala-operador-sufix

A medida que voy aprendiendo más sobre el lenguaje **scala**, se me ocurren nuevas formas de expresar la función factorial.

La *"expresividad"* del lenguaje permite usar operadores para crear código más corto. Por ejemplo, la función factorial con *"plegados"* (*"folds*") que poníamo en un artículo anterior se podría expresar así:

```scala
def fact(n:Int)=(BigInt(1) /: (1 to n))(_*_)
```

En esta expresión, hacemos el *plegado* de la secuencia `(1 to n)` sobre el valor inicial `BigInt(1)` con la operación `(_*_)` (multiplicación). Se ve rara, pero una vez profundizas en scala se ve como algo normal.

Otra de las opciones de scala es poder usar casi cualquier carácter como indentificador, lo que nos facilita la creación de DSL (*"Lenguajes Específicos al Dominio"*). Una de estas posibilidades sería crear el operador *sufix* de la función factorial, de modo que el cálculo de factorial de `n` se pudiera expresar como `n!`. Para ello aprovechamos el mecanismo que tiene scala para conversión automática de tipos de datos:

```scala
class Factorizer(n:Int){
    def ! = (BigInt(1) to n).product
}

implicit def int2fact(n:Int)=new Factorizer(n)

println("5!="+(5!))
```

La explicación es bien sencilla: como no encuentra el método `'!'` en el tipo `Int`, busca entre las conversiones otros tipos que lo puedan tener, en este caso `Factorizer`. Una vez hecha la conversión, ejecuta el operador.
