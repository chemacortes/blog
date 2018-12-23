Title: Mutable o inmutable, he ahí el dilema
Date: 2013-03-22 22:02
Modified: 2018-07-25 01:09:30
Author: Chema Cortés
Category: Python
Slug: mutable-o-inmutable-he-ahi-el-dilema

!!! INFO
    Disponible también como [ipynb](http://nbviewer.jupyter.org/5224623)

Quien se enfrenta a la documentación de python por primera vez se pregunta porqué esa insistencia en mantener tipos de datos duplicados en versiones mutables e inmutables. Tenemos listas y tuplas que casi hacen lo mismo. En python3, tenemos el tipo inmutable `bytes` y el mutable `bytearray`. ¿Qué sentido tiene tener _"duplicados"_ algunos tipos en sus dos versiones? La única explicación que se puede encontrar en la documentación es que los tipos inmutables son más apropiados para usarlos como índices en diccionarios. No parece mucha ventaja para la complejidad que aporta.

En este artículo veremos qué implica la _mutabilidad_ de un tipo de dato y en qué puede sernos útil usar un tipo mutable u otro inmutable.

## ¿Qué es lo que cambia?

Antes de explicar nada, veamos si somos capaces de saber qué está cambiando. Veamos dos códigos muy similares:

~~~python
>>> a = (1, 2, 3, 4)
>>> a += (5, 6, 7)
>>> print(a)
(1, 2, 3, 4, 5, 6, 7)
~~~

~~~python
>>> a = [1, 2, 3, 4]
>>> a += [5, 6, 7]
>>> print( a )
~~~

Parece que ambos códigos hagan lo mismo: añadir un fragmento, en sus versiones tupla y lista, respectivamente. Vamos a analizarlo mejor. Para saber qué pasa, usemos la función `id()`. Esta función devuelve un identificador de un objeto de tal modo que si dos objetos tienen el mismo identificador, entonces son el mismo objeto.

~~~python
>>> a = (1, 2, 3, 4)
>>> print(id(a))
192021604
>>> a += (5, 6, 7)
>>> print(id(a))
189519828
~~~

~~~python
>>> a = [1, 2, 3, 4]
>>> print(id(a))
189780876
>>> a += [5, 6, 7]
>>> print(id(a))
189780876
~~~

En la versión tupla, se ha creado una nueva tupla para realizar la operación, mientras que en la versión lista se ha usado la misma lista, modificándose con el resultado. Si cambiamos el operador `+=` por una versión más explícita tal vez se vea mejor:

~~~python
>>> a = (1, 2, 3, 4)
>>> a = a + (5, 6, 7)
~~~

~~~python
>>> a = [1, 2, 3, 4]
>>> a.extend([5, 6, 7])
~~~

Al operar con tuplas, los operandos no cambian de valor, creándose una nueva tupla como resultado de la operación. Podríamos sustituir toda la operación por el resultado final y el código funcionaría igual. En el caso de las listas, la lista se modifica _"in situ"_ durante la operación. En estos casos, cambiar la expresión por el resultado final no garantiza que el programa funcione igual. Se necesita pasar por todos y cada uno de los estados intermedios para asegurar que todo funcione igual.

Esta propiedad de poder cambiar una expresión por su resultado final es conocida por [Transparencia referencial][1] en programación funcional. Por lo general, los tipos inmutables se adecúan mejor a operaciones de cálculo donde el resultado final depende únicamente de los argumentos de entrada. Por otro lado, los tipos mutables son útiles para salvaguardar estados intermedios necesarios para la toma de decisiones durante la ejecución de un programa.

Por lo general, se saber elegir un tipo mutable o su homólogo inmutable es todo un arte. Ante la duda, los tipos inmutables son más fáciles de rastrear. Así mismo, veremos en próximos artículos que los tipos inmutables ayudan bastante en programación concurrente, por si estás pensando en programación multiproceso.

[1]: http://en.wikipedia.org/wiki/Referential_transparency_(computer_science) "Referential Transparency"

## Ejemplos de tipos propios

La mutabilidad e inmutabilidad va más allá de los tipos estándar de python. Nosotros mismos podemos hacer nuestras propias clases mutables o inmutables, según nuestras necesidades.

Pongamos que creamos una clase `Point` para definir puntos, junto con unas sencillas operaciones para sumar, restar y desplazar. Nuestra idea es poder usar estos objetos en expresiones, por lo que es práctica común que toda operación devuelva el resultado como un punto para seguir encadenando operaciones.

Una versión _"mutable"_ del objeto sería así:

~~~python
class PointMutable(object):
    def __init__(self, x, y):
        self.x=x
        self.y=y

    def __repr__(self):
        return "<Point(%d,%d)>" % (self.x, self.y)

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        return self
~~~

En todas las operaciones, operamos el objeto consigo mismo y lo retornamos como resultados. Si probamos, vemos que no funciona tal como se esperaba:

~~~python
>>> p1=PointMutable(1, 1)
>>> p2=PointMutable(-1, 1)
>>> print p1.move(1, 1) - (p1 + p2).move(2, 2)
<Point(0,0)>
~~~

Devuelve `<Point<0,0>` independientemente de los valores iniciales y de los desplazamientos que demos. Al ser nuestro objeto mutable, cada operación lo va cambiando. Al final, toda la expresión se reduce a una simple resta `p1-p1`, que sería la última operación y que da siempre `<Point(0,0)>`. No parece que sea el resultado esperado.

Debemos adoptar una táctica más defensiva: el objeto nunca debe cambiar durante el cálculo. Como resultado de cada operación deberemos devolver una nueva instancia y que el estado de ésta, o sea, sus atributos, no se alteren a lo largo del cálculo:

~~~python
class PointInmutable(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "<Point(%d,%d)>" % (self.x, self.y)

    def __sub__(self, other):
        return PointInmutable(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return PointInmutable(self.x + other.x, self.y + other.y)

    def move(self, dx, dy):
        return PointInmutable(self.x + dx, self.y + dy)
~~~

~~~python
>>> p1=PointInmutable(1, 1)
>>> p2=PointInmutable(-1, 1)
>>> print p1.move(1, 1) - (p1 + p2).move(2, 2)
<Point(0,-2)>
~~~

Siendo perfeccionistas, deberíamos blindar mejor los atributos de la clase para hacerlos de _sólo lectura_ mediante `properties`.

En este ejemplo hemos podido ver los resultados imprevisibles que podemos tener si abusamos de la mutabilidad. Estos problemas se ven incrementados si hubiera varios hilos de ejecución y cada hilo estuviera modificando las mismas variables comunes. Lamentablemente, es un caso bastante común debido a una mala previsión a la hora de iniciar un proyecto de desarrollo. Pero ésto lo veremos en un próximo artículo.
