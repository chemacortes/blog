Title: Descriptores - Parte 1
Date: 2011-06-19 16:57
Author: Chema Cortés
Category: Python
Tags: descriptor, técnicas dinámicas
Slug: descriptores-parte-1

Cuando accedemos a los atributos de un objeto en python, a veces existen unos intermediarios casi imperceptibles llamados *"descriptores"* que son los responsables últimos del funcionamiento de la programación orientada a objetos. Están detrás de *propiedades*, métodos, métodos estáticos, métodos de clase y del mecanismo `super()` responsable de la herencia múltiple. Su labor es imprescindible y, sin embargo, son los grandes desconocidos del lenguaje.

#Protocolo "descriptor"

Por protocolo *"descriptor"* se entiende la sustitución de un atributo por un objeto que intermedia en los accesos a ese atributo. Tal vez, las *propiedades* (`property`) puedan ser el ejemplo más visible de los descriptores, pero veremos que los descriptores están más presentes de lo podemos pensar.

Como descripción formal del protocolo descriptor, podemos decir que un descriptor es todo objeto que tenga definido al menos uno de estos tres métodos:

```python
descr.__get__(self, obj, type=None) --> value

descr.__set__(self, obj, value) --> None

descr.__delete__(self, obj) --> None
```

Respectivamente, serían los métodos para obtener, asignar y borrar un atributo del objeto `obj`.

Podemos distinguir dos tipos de descriptores:

- **Descriptor de datos** (*data descriptor*): cuando tiene definidos los métodos `__get__` y `__set__`. Es el que usaremos para acceder y cambiar el valor de un atributo.
- **Descriptor de no-datos** (*non-data descriptor*): cuando sólo tiene definido el método `__get__`. Su uso será casi exclusivo para acceso a los métodos de un objeto.

Como veremos más adelante, distinguir entre estos dos tipos de descriptores es muy importante, ya que cada uno tiene distinto orden de preferencia cuando se buscan atributos en una jerarquía de clases.

#Implementación de los "Descriptores de Datos"

Empecemos por un ejemplo:

```python
class Desc(object):
    def __init__(self, mul):
        self.mul=mul
    def __get__(self, obj, cls=None):
        return obj.value*self.mul

class C(object):
    a12=Desc(12)
    a200=Desc(200)
    
    def __init__(self,value):
        self.value=value

c=C(2)
print c.value, c.a12, c.a200  #--> 2 24 400
```

Los atributos `a12` y `a200` están definidos por instancias del descriptor `Desc()`. Cuando accedemos a estos atributos, en lugar de devolvernos el descriptor, nos devuelve el valor resultante del método `__get__` del descriptor.

De modo más explícito, sería:

```python
c.a12 --> c.a12.__get__(c)
```

Al no estar definido el método `__set__`, se pueden reasignar estos atributos sin mayor problema, aunque dejarían así de estar controlado por el descriptor:

```python
c.a12=12
```

Para completar el protocolo de *descriptor de datos* basta añadir un método `__set__`:

```python
class Descrip(object):
    def __init__(self, mul):
        self.mul=mul
    def __get__(self, obj, cls=None):
        return obj.value*self.mul
    def __set__(self, obj, value):
        obj.value=value
```

La asignación anterior, se nos convertiría en:

```python
c.a12=12 --> c.a12.__set__(c, 12)
```

Como se intuye, el descriptor tiene aquí total control sobre el valor final que se guardará como atributo. Como posible utilización, se pueden crear atributos de sólo lectura, para lo que bastaría con que el método `__set__` genere un error `AttributeError` si se intenta modificar el atributo:

```python
class Descrip(object):
    def __init__(self, mul):
        self.mul=mul
    def __get__(self, obj, cls=None):
        return obj.value*self.mul
    def __set__(self, obj, value):
        raise AttributeError
```

Tan sólo falta añadir el método `__delete__` para completar el protocolo. No hay que olvidarse de este método si queremos que un atributo de sólo lectura aún pueda ser modificado mediante un borrado previo a su reasignación:

```python
class Descrip(object):
    def __init__(self, mul):
        self.mul=mul
    def __get__(self, obj, cls=None):
        return obj.value*self.mul
    def __set__(self, obj, value):
        raise AttributeError
    def __delete__(self, obj):
        del self

c=C(2)

print c.a12 #--> 24

c.a12=100 #ERROR: AttributeError

del C.a12
c.a12=100

print c.a12  #--> 100 (no descriptor)
```

#Saltarse al descriptor

Llegados aquí, se nos plantea una pregunta: ¿hay algún modo de acceder a los atributos sin pasar por su descriptor?

Y no es para nada una pregunta caprichosa. El descriptor necesita algún modo de acceder a los atributos que está gestionando sin tener que pasar por sí mismo. Tal vez, se podría hacer a través del diccionario del objeto, accesible como `__dict__`:

```python
c.__dict__["a12"]=100  #equivalente a c.a12=100
```

Si lo pruebas, verás que no funciona. Cuando se busca un atributo, primero se busca entre los atributos de la clase antes de mirar en el diccionario de la instancia. Este orden de prioridades lo veremos en el próximo artículo cuando veamos el funcionamiento interno de un descriptor.
