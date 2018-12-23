Title: Dobleces en python
Date: 2013-02-27 21:39
Author: Chema Cortés
Category: Python
Slug: dobleces-en-python

En el [último artículo][1] del blog contaba en qué consistía *doblar código*[^1]:

> "...un código que se pliega sobre sí mismo. Un código que te
> lleva desde un principio a un final por el camino más corto."
	
Para ilustrar este concepto voy a usar un trozo de código python que se ve frecuentemente entre los programadores recién llegados de otros lenguajes:

<sub><em>NOTA: se usará python 3.x para los siguientes ejemplos</em></sub>

```python
def listar(args):
    num=len(args)
    i=0
    while(i<num):
        x=args[i]
        print(format(len(x)," 5d"), x)
        i+=1

fich=open("fichero.txt")
lineas=fich.readlines()
listar(lineas)
```

Resumen: se define una función para imprimir en pantalla la lista de líneas leídas de un fichero, precedidas con el número de caracteres que tiene la línea.

Quien tenga algo de experiencia con python seguramente vea raro este código, incluso lo califique como *"poco pythónico"*. Nombrar a la función `listar`, como verbo, es señal de que el programador proviene de un lenguaje de *programación imperativo*. El programador ha buscado en python las mismas estructuras de control que tenía en su lenguaje de origen y sólo ha encontrado familiar la estructura `while`.

Rebuscando un poco más, tal vez encuentre cómo se usan los bucles `for` en python:

```python
def listar(args):
    num=len(args)
    for i in range(0,num):
        x=args[i]
        print(format(len(x)," 5d"), x)
```

Un bucle `for` se caracteriza por concentrar en una sentencia todo el control del bucle, una gran ayuda visual para quien vaya a leer este código. La variable de control solo se modifica en la sentencia `for`, lo que evita errores.

Analizando más detenidamente, el bucle `for` itera sobre una secuencia de enteros dada por `range(0,num)`, de donde se sacan los índices con los que acceder a cada elemento de la lista `args`. Ésta sería la visión clásica de cómo operar con `arrays`.

Pero esta visión ha evolucionado con el tiempo hasta llegar al concepto de *"Colección"* que ya poseen casi todos los lenguajes, bien en su sintaxis, bien como librería estándar. Una *"Colección"* consiste en un grupo de objetos sobre los que puede iterar. `range(0,num)` sería una colección ordenada de números. El siguiente paso a dar sería iterar directamente sobre la lista:

```python
def listar(args):
    for x in args:
        print(format(len(x)," 5d"), x)
```

Con este código hemos conseguido un doble objetivo, mejorar la legibilidad y darle más robustez al despreocuparnos por los índices de acceso. Los índices de acceso fuera de límites suelen ser origen de multitud de errores.

Pero tenemos algo más: al no usar índices hemos generalizado el uso de la función por cualquier secuencia, generador o [iterador][3]. Concretamente, los objetos `files` cumplen con el protocolo iterador, por lo que sería posible pasarlo directamente a esta función sin necesidad de volcar todas las líneas del fichero a una lista:

```python
def listar(it):
    for x in it:
        print(format(len(x)," 5d"), x)

listar(open("fichero.txt"))
```

Con este último doblez hemos ganado concisión. Pero sobre hemos ahorrado recursos ya que no necesitamos leer todo el fichero en memoria. La lectura del fichero se hará progresivamente en el momento que se solicite la siguiente línea, por lo que este código debería funcionar incluso con ficheros enormes, independiente de la cantidad de memoria disponible. Sólo se empleará la memoria suficiente para cachear una pocas líneas para ir renovándolas a medida que se prosiga la lectura del fichero.

Es un buen momento para comparar esta versión del código con la original de la que hemos partido.

##Programación Funcional

Entre doblez y doblez, hemos perdido algunas variables intermedias superfluas. Esta *manía* por deshacerse de variables intermedias es señal de estar aproximándonos a un estilo de *programación funcional*.

Una posible definición de *"Programación Funcional"* sería como *aquella programación que difiere la evaluación de una expresión hasta el momento último en el que se vaya a usar su valor*.

Para este propósito, la expresión no puede depender de factores externos como variables globales o cambios de estado. No sabemos cuándo será evaluada una expresión. Lo único posible es hacer depender el resultado de una expresión en función del valor de otra, lo que se conoce por *"Composición de funciones"* (y de ahí el nombre de programación funcional).

Este modo de diferir la evaluación es lo que hicimos con el iterador fichero, cuyas líneas no se leían hasta el momento preciso. La pregunta es ¿podemos mejorar la orientación funcional de nuestro código?

La función `listar` no devuelve nada, tan sólo busca un efecto colateral. Es lo que se conoce en otros lenguajes como *"procedimiento"* (*procedure*). En nuestra metáfora de "pliegues", una función que no devuelve nada la podríamos considerar como un "corte", ya que no podemos hacer nada más a partir de aquí.

¿Qué pasaría si queremos cambiar la línea que se imprime en pantalla? ¿Y si queremos parar después de imprimir un número de líneas? En este punto, lo mejor es "desdoblar" el código y darle una orientación más funcional:

```python
from itertools import islice

def lineas(it):
    for x in it:
        yield ("{: 5d} {}".format(len(x), x))

it=lineas(open("pr.py"))

for n, l in enumerate(islice(it,5)):
    print(n, "|", l)
```

La función `listar` ha pasado a ser el iterador `lineas` que retorna las líneas ya formateadas. Asimismo, se ha cambiado la función `format` por el método `format` de los `strings` con el que se pueden formatear mejor varios valores a la vez. La impresión de las líneas en pantalla se deja para el último momento, cuando se necesita ver el resultado. Es en este momento cuando se decide cuántas líneas se van a imprimir, que es lo que hace el `islice` acortando el iterador `lineas` a 5 iteraciones. También se usa el iterador `enumerate` para ir enumerando las líneas a medida que las obtenemos.

Como se ve, una orientación funcional permite encadenar varias operaciones sin necesidad de mantener estados intermedios[^2]. Además de lo que supone de ahorro de recursos, no tener que mantener un contexto con los estados intermedios hará más sencillo migrar la ejecución de un proceso a otro en programación concurrente (eg: *multihilo*). Hoy en día, tal como evolucionan los ordenadores, quien no programe pensando en la ejecución concurrente terminará programando dos veces.


[^1]: Puede que prefieras usar el término [*"refactorizar"*][2], pero he pensado que es mejor dejar este término para la programación orientada a objeto y usar *"doblez"* para dar una idea más afín a la programación funcional.
[^2]: En realidad, no es del todo cierto que la función no dependa de estados externos ya que el iterador `it` que hemos pasado como argumento podría cambiar externamente entre iteraciones.

[1]: {filename}collage-vs-origami.md "Collage vs. Origami"
[2]: http://es.wikipedia.org/wiki/Refactorización "Refactorización"
[3]: http://docs.python.org/3/library/stdtypes.html#iterator-types "Tipo iterador"
