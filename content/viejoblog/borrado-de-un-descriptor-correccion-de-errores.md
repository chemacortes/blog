Title: Borrado de un descriptor (corrección de errores)
Date: 2013-07-13 14:00
Modified: 2018-07-25 01:30:02
Author: Chema Cortés
Category: Python
Tags: descriptor, técnicas dinámicas
Slug: borrado-de-un-descriptor-correccion-de-errores

Tengo que hacer algunas correcciones a la serie de artículos sobre *descriptores*, en concreto sobre el método `__delete__` del protocolo *descriptor*.

Primero, aclaremos cómo funciona el método `__delete__` y en qué se diferencia de `__del__`. No se trata de métodos *destructores* tal y como se entiende en otros lenguajes de programación orientados a objeto. En python, **todo objeto está vivo mientras esté referenciado**. Sólo cuando se pierda la última referencia se procederá a la destrucción y borrado del objeto en memoria por parte del *recolector de basura*.

Por ejemplo, veamos el siguiente código:

~~~python
class Miclase(object):

    def __del__(self):
        print "instance deleted"

a = Miclase()
b = a
del a

print b
print "Come on"
b = 1
print "END"
~~~

De su ejecución, podemos comprobar que el método `__del__` no se invoca justo en el momento de hacer `del a`, si no cuando se pierde la última referencia al asignar otro valor a la variable `b`. La sentencia `del a` no *destruye* el objeto, tan sólo desliga el objeto de la etiqueta `a` que lo referenciaba. Por ese motivo, es inexacto hablar en python de "variable de memoria", como se entiende en otro lenguajes. Tan sólo cambiamos de una referencia de un objeto a otro, sin destruir su valor anterior.

## Revisión del protocolo descriptor

En un [anterior artículo][1] distinguía entre descriptores de datos y de no-datos. Hay que aclarar que un descriptor de datos "es también el que sólo tiene definido un método `__delete__`, aunque no tenga método `__set__`". ¿Para qué puede sernos útil tener uno sin el otro?

Un descriptor de datos sin método `__set__` no tiene forma de impedir que el atributo/método que implementa sea sustituído por otro objeto (por ejemplo, por otro descriptor). El método `__delete__` nos daría la última opción de liberar recursos que ya no vayamos a usar antes de desaparecer el descriptor. Pero, independiemente de lo que haga, el método `__delete__` indicaría que el descriptor puede ser sustituido. En definitiva, se comportaría como un *descriptor de no-datos*, pero con las diferencias en la invocación entre estos dos tipos de descriptor[^1].

Para aclarar las cosas, veamos qué estaba mal en el [ejemplo][1] que puse en su momento  sobre el uso de `__delete__` (he cambiado algunos nombres para que se vea más claro):

~~~python
class Desc(object):

    def __init__(self, mul):
        self.mul = mul

    def __get__(self, obj, cls=None):
        return obj.value * self.mul

    def __set__(self, obj, value):
        raise AttributeError

    def __delete__(self, obj):
        del self

class Miclase(object):

    a12 = Desc(12)
    a200 = Desc(200)

    def __init__(self, value):
        self.value = value


c = Miclase(2)

print c.a12 #--> 24

c.a12 = 100  # ERROR: AttributeError

del Miclase.a12
c.a12=100

print c.a12  #--> 100 (no descriptor)
~~~

La idea era que se pudiera borrar el descriptor de datos para sustuirlo por otro valor. Tal como señalaba Cristian en un comentario al respecto, este ejemplo parece funcionar con o sin el método `__delete__` en el descriptor.

Funciona siempre debido a que con `'del Miclase.a12'` estamos borrando la referencia al descriptor que tiene la clase, sin pasar por el protocolo descriptor. La particularidad de los descriptores es que *viven* en la clase, pero se invocan desde la instancia. Con `'del Miclase.a12'` estamos saltándonos el protocolo descriptor para acceder directamente al atributo de la clase[^2].

Además, este código no funcionaría nunca:

~~~python
    def __delete__(self, obj):
        del self
~~~

Si la idea era borrar el objeto `self`, referencia al descriptor, podemos quitarnos esa idea ya que el comando `del` borra la referencia del *scope* local donde se encuentra. **¡No es un destructor!** En realidad, todas las variables locales son borradas al finalizar el método. En este caso en concreto, también la variable local `obj` será borrada aunque no se indique explícitamente.

Otra cuestión a tener en cuenta es que los atributos de clase son compartidos por todas sus instancias. Si en algún momento alteramos un descriptor (por ejemplo, borrándolo), entonces todas las instancias sufririan el mismo cambio. No parece que sea el efecto buscado.

La gran pregunta es *entonces, ¿cómo podemos aprovecharnos del método `__delete__`?*

Para sacarle algún partido, el descriptor debería comportarse de forma distinta según sea la instancia que lo invoca. Definido así el descriptoor, entonces podríamos usar el método `__delete__` para simular el borrado del atributo para esa instancia, sin que el descriptor pierda su funcionalidad.

Un ejemplo para ilustrar ésto sería:

~~~python
from weakref import WeakKeyDictionary

class Desc(object):

    def __init__(self):
        self.data = WeakKeyDictionary()

    def __get__(self, obj, cls=None):
        if obj not in self.data:
            raise AttributeError
        total = sum(x for x in self.data.values())
        return (self.data.get(obj), total)

    def __set__(self, obj, value):
        if obj in self.data:
            raise AttributeError
        self.data[obj] = value

    def __delete__(self, obj):
        del self.data[obj]

class Miclase(object):

    value = Desc()


a = Miclase()
b = Miclase()

a.value = 2
b.value = 5

print a.value  #--> (2, 7)
print b.value  #--> (5, 7)

a.value = 100  # ERROR: AttributeError

del a.value
a.value = 11

print a.value  #--> (11, 16)
print b.value  #--> (5, 16)

del b

print a.value  #--> (11, 11)

~~~

El descriptor mantiene un diccionario *weak* con valores asignados para cada instancia de la clase. Usamos para ello un *WeakKeyDictionary* que tiene la particularidad de relajar la referencia al objeto, de modo que si todas las referencias al objeto son borradas en el programa, también es borrada la referencia que conservaba el diccionario.

En este ejemplo, el método `__get__` devuelve el valor del atributo si el objeto está en el diccionario, si no da error. El método `__set__` asigna un valor al atributo sólo si el objeto no existe. Para ver mejor el funcionamiento, el método `__get__` devuelve una tupla con el valor del atributo y la suma de todos los atributos.

Ejecuntado el ejemplo, creamos dos instancias y les asignamos un valor al atributo controlado por el descriptor. Una vez asignado un valor, ya no podemos cambiarlo. La única opción será borrar el atributo y volverlo a asignar.

También se puede comprobar que, cuando borramos el objeto `b`, la suma de todos los atributos se actualiza a las instancias que aún quedan *vivas*.

En el borrado del atributo se usa el método `__delete__` del descriptor; en el borrado de la instancia, el método `__del__` (si existiera).

## Referencia

No quisiera acabar este artículo sin añadir una referencia sobre este tema que os recomiendo leer, con algunas recetas para aprovechar el uso de los descriptores:

["Python Descriptors Demystified"][3] by [Chris Beaumont](http://chrisbeaumont.org/)

[3]: http://nbviewer.jupyter.org/gist/ChrisBeaumont/5758381/descriptor_writeup.ipynb

[^1]: Comentado en los anteriores [artículos sobre descriptores][2].
[^2]: Un modo de impedir el borrado de atributos de una clase sería aplicando el protocolo descriptor con metaclases, pero pienso que estaríamos complicándolo todo demasiado para el beneficio que pudiera obtenerse a cambio.

[1]: {filename}descriptores-parte-1.md
[2]: {tag}descriptor
