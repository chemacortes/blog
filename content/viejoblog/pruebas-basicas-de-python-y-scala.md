Title: Pruebas básicas de python (y scala)
Date: 2012-10-25 17:04
Author: Chema Cortés
Category: Python
Tags: python, scala, programming
Slug: pruebas-basicas-de-python-y-scala

Como continuación del artículo ["Cómo contratar a un programador de python"][1] voy a dar las soluciones a algunas de las pruebas básicas que comentaba del proceso de selección. Añado también las soluciones sobre cómo sería con *scala* y de paso comparamos ambos lenguajes[^1].

##Prueba del "Hello, World!"

Desde que se inventó el lenguaje C, la prueba del `"Hello, World!"` es la prueba que inicialmente caracteriza a un lenguaje. Y en python sería:

```python
print "¡Hola, Mundo!"
```

Lo que hay que saber es que este código no funciona en python3 y será lo primero que te pregunte el seleccionador. En python3, el comando `print` se convierte en una función, por lo que se debe añadir los paréntesis:

```python
print("¡Hola, Mundo!")
```

Con esta introducción, el seleccionador te puede preguntar alguna cosa más sobre el comando `print`, como si se puede usar con cualquier objeto o si se puede sacar fácilmente una salida tabulada.

En scala, la respuesta también es simple:

```scala
println("¡Hola, Mundo!")
```

`println` es una función, como es lógico al tratarse de un *lenguaje funcional*. Un seleccionador te puede preguntar por el sufijo `ln`, que no es otra cosa que añadir un salto de línea en la salida. Este código es equivalente a:

```scala
print("¡Hola, Mundo!\n")
```

Se puede ver al final una expresión de escape que representa al salto de línea, universalmente aceptada por un buen número de lenguajes (python incluído).

##Detector de palíndromos

Un palíndromo sería una frase que resulta igual leída del principio al final, que del final al principio. Algunos ejemplos:

```text
A man, a plan, a canal: Panama!
Dábale arroz a la zorra el Abad
```

Para hacer un detector de palíndromos en python tenemos que hacer una función que lo primero que haga sea filtrar todos los espacios en blancos y los signos de puntuación de la frase, convertir todas las letras a minúsculas (o mayúsculas) y comprobar luego si la frase es igual en un sentido y otro:

```python
def isPalindrome(frase):
    frase_limpia=[c.lower() from c in frase if c>="A"]
    return frase_limpia==frase_limpia.reverse()
```

Como primera aproximación puede valer. Se filtra la frase para que sólo aparezcan letras (`c>="A"`), quitando espacios y signos de puntuación. También se ha convertido a minúsculas con `c.lower()` para hacer mejor la comparación. El problema es que no convierte las vocales con tilde a vocales sin tilde, con lo que el palíndromo *"Dábale arroz a la zorra el Abad"* no lo va a detectar bien. El *"candidato"* debe darse cuenta de ello e intentar explicar algún modo de resolverlo (cuya resolución completa quedaría fuera de la prueba real y del presente artículo[^2]).

En scala sería algo así:

```scala
def isPalindrome(frase:String):Boolean={
    val frase_limpia=frase.filter(_>='A').toLowerCase
    frase_limpia==frase_limpia.reverse
}
```

Aquí todas las operaciones se han hecho con el tipo `String`, sin necesidad de pasar a una lista como en python. La última sentencia de la función será el resultado que devuelve la función. En sí, esta función sería correcta, pero usar una variable intermedia como `frase_limpia` para guardar un estado intermedio va en contra de la filosofía de la programación funcional. Un programa funcional *intenta retrasar todo lo que se pueda la evaluación del resultado con el fin de evitar posibles efectos colaterales*. Lo ideal sería que sólo se hiciera la *evaluación* en la última sentencia de la función.

Una forma de hacerlo más *"funcional"*:

```scala
def isPalindrome(frase:String):Boolean={
    val f= (s:String)=>s==s.reverse
    val g= (s:String)=>s.filter(_>='A').toLowerCase
    (f compose g)(frase)
}
```

...o todo junto en una línea:

```scala
def isPalindrome(frase:String):Boolean=
    ((s:String)=>s==s.reverse)(frase.filter(_>='A').toLowerCase)
```


##Expresión regular para encontrar teléfonos en un texto

Lo más simple es buscar 9 dígitos seguidos y sin espacios: `"\d{9}"`

El examinador probablemente quiera que te esfuerces algo más. Te puede decir que esa expresión no sirve para localizar teléfonos como el `+34 666 010101` y quiere saber cómo se podría hacer. La cosa se complica bastante, aunque no es imposible. En este momento NUNCA digas que haría falta leerse bien la documentación y que tendrías que investigar un poco, suena muy mal. Lo de *investigar* da la idea que vas a buscar una solución por internet, que acabarás en un blog como éste y que vas a copiarte la solución sin siquiera leer cómo funciona.

Más vale que busques otra alternativa, aunque sea sin usar expresiones regulares. Lo que realmente interesa al entrevistador es que tengas ideas propias y originales que se puedan aplicar para resolver el problema que se te plantea.

A continuación pongo una posible solución, aunque te aconsejo que la estudies antes de aplicarla literalmente a tu código:

        "((\+34 )?\d{3} ?\d{6})"


##Una conversión de lista de tuplas a diccionario

Este es uno de esos casos que cuesta más explicar el problema que su solución. Se pretende ver si el candidato comprende realmente los conceptos que se tratan, si sabe lo que es una tupla y un diccionario, y si tiene claro el concepto de *"mapping"* por el cuál se contruye el diccionario.

La solución empieza por poner en dependencia el segundo elemento del primero:

```python
lista=[("a",1),("b",2),("c",3)]
dic=dict(lista)
```

En scala es muy parecido:

```scala
val lista=List(("a",1),("b",2),("c",3))
val dic=lista.toMap
```

Por complicarlo algo más, se puede pedir que se repita el ejercicio, pero con tuplas de más de dos elementos, con el primero como clave del *mapping*:

```python
lista=[("a",1,2,3),("b",10,20,30),("c",100,200,300)]
dic=dict((x[0],x[1:]) for x in lista)
```

En scala es algo más complicado. Lo que en python se entiende por tupla (una secuencia inmutable), en scala son en realidad las listas. Las listas mutables, como se entienden en python, son instancias de la clase `MutableList`. Las tuplas de scala se usan para paso de parámetros y poco más:

```scala
val lista=List(List("a",1,2,3),List("b",10,20,30),
  List("c",100,200,300))

val dic=lista map {x => x.head->x.tail} toMap
```

Aquí se ve el uso de los atributos `head` y `tail` para manejar listas que son tan característicos de los lenguajes funcionales.

Las últimas versiones de Scala incorporan la "comparación de patrones" (*"pattern matching"*) que consiguen hacer algo más legible el código:

```scala
val dic=lista map {case h::t => h->t} toMap
```

No parece que haya variado mucho. La potencia de los patrones está en poder realizar distintas operaciones según el tipo de los parámetros. En otros lenguajes se necesitaría incorporar expresiones condicionales o sobrecarga de operadores.

Por ejemplo, imagina que la lista tuviera elementos extra como cadenas y números:

```scala
val lista=List(List("a",1,2,3),List("b",10,20,30),
  List("c",100,200,300),List(1,2,3,4,5),List(1), "Hola", 1.5)

val dic=lista collect {
    case h::t => h->t
    case s:String => s->List()
   } toMap
```

Vemos el resultado:
```text
//for((k,v)<-dic) println(k,v)
(Hola,List())
(1,List())
(a,List(1, 2, 3))
(b,List(10, 20, 30))
(c,List(100, 200, 300))
```

En el primer patrón, `h::t` (llamado de *extracción de lista*), sólo encajarán los items que son listas; en el segundo patrón `s:String` sólo encaja la `String "Hola"`; mientras que el último elemento de la lista, el `double 1.5`, no coincide con ningún patrón y será filtrado por el método `collect`.

Si intentamos hacer lo mismo con python nos saldría un código bastante menos legible:

```python
lista=[("a",1,2,3),("b",10,20,30),("c",100,200,300),(1,),"Hola",1.5]

dic=dict( ((x[0],x[1:]) if isinstance(x,tuple) else (x,()))
    for x in lista if isinstance(x, (tuple, basestring)))
```

##Conclusión

Con estos ejemplos tan sólo he querido darte una idea de qué cosas podemos encontrarnos en una prueba de selección. En programación, debería interesar más la capacidad resolutiva del *candidato* que su nivel de conocimientos. Una solución innovadora o que aporte otro punto de vista no contemplado en un principio suele ser de más valor que dar la solución correcta. Busca distintos ejemplos de resolver los mismos problemas, incluso en lenguajes de programación diferentes, y estarás preparado para todo reto que se te presente.

---

[^1]: Si te preguntas porqué *scala*, la respuesta simple sería 
*porque es el lenguaje que estoy aprendiendo ahora mismo*. Pero si realmente te preguntas qué puede aprender un programador python de un lenguaje como scala, no te pierdas el próximo artículo.

[^2]: Busca en la lista [python-es](http://mail.python.org/mailman/listinfo/python-es)

[1]: {filename}como-contratar-un-programador-de-python.md "Cómo contratar un programador de python"
