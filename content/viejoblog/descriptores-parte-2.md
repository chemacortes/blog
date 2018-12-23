Title: Descriptores - Parte 2
Date: 2011-06-21 01:26
Author: Chema Cortés
Category: Python
Tags: descriptor, técnicas dinámicas
Slug: descriptores-parte-2

#¿Cómo funciona un descriptor?

Todos los objetos y todas las clases que derivan de `object`[^1] adquieren de él un método llamado `__getattribute__`. Siempre a través de este método se accede a los atributos, y es en este método donde se hace toda la *magia* de los descriptores, de modo que un acceso al atributo `obj.x` se transformará en una llamada a `type(obj).__dict__['x'].__get__(obj, type(obj))` si el atributo se trate de un descriptor. Una expresión casi ininteligible que va a requerir alguna que otra explicación. Lo importante es saber que al sobrecargar el método `__getattribute__` deberemos cuidarnos de invocar al método de la clase padre si queremos que los descriptores sigan funcionando con normalidad.

#Atributos de un objeto

De todos los atributos que tiene un objeto python, algunos son **"Atributos especiales"** que aporta python para su funcionamiento interno como son `__class__` o `__bases__`. Estos atributos son bastante antipáticos de manejar ya que, o bien no son reportados por la función `dir()`, o bien tienen restricciones para ser modificados.

Por otro lado, están los atributos definidos *dinámicamente* por el programa que forman lo que se conoce como **"diccionario del objeto"**. Estos atributos se guandan en el (*también*) atributo `__dict__`.

Los **"atributos de tipo"** son los atributos asociados a un objeto por pertenencia a una clase. Estos atributos pueden estar enmascarados por los atributos del diccionario del objeto, algo muy útil cuando se aplican *"técnicas dinámicas"* de parcheo.

Hay que tener en cuenta que algunos de los *tipos estándar* como `list`,`tuple`,`dict`,... no tienen atributo `__dict__` con lo que no tienen diccionario donde añadir o suplantar atributos dinámicamente. La única opción pasa por derivar clases a partir de ellos para añadir allí los atributos deseados.

#Búsqueda de atributos

Al buscar un atributo `obj.attr`, se sigue un orden determinado de prioridad según el tipo de atributo que se esté buscando:

1. **Atributos especiales**: son los que tienen mayor prioridad.

2. **Descriptores de datos**: se buscan en el diccionario de la clase (`obj.__class__.__dict__`) y en todos los diccionarios de las clases padre. Si se encuentra, se retorna el resultado del descriptor (la expresión tan chula que puse al principio del artículo). Si no es un descriptor de datos, entonces se ignora y se sigue buscando.

3. Atributos del **diccionario del objeto**: se busca el atributo en el diccionario del objeto (`obj.__dict__`). Si `obj` fuera una clase (`==isinstance(obj,type)`), entonces también se buscaría en los diccionarios de las clases padre (`obj.__bases__`) y, de ser un descriptor de datos, se devolverá el resultado del descriptor en su lugar.

4. **Descriptores de no-datos**: se repite el paso 2, pero esta vez se buscan descriptores de no-datos.

5. **Método `__getattr__`**: por último, si no ha habido éxito en la búsqueda del atributo, se intenta invocar el método `__getattr__`, de existir, para delegar en él.

6. Si todo ha fallado, se termina la búsqueda retornando un error `AttributeError`.

En resumidas cuentas, se priorizan los descriptores de datos a las variables de instancia, las variables de instancia a los descriptores de no-datos y, con la más baja prioridad, se invocaría el método `__getattr__`.

Remarcar la diferencia que hay entre un descriptor de datos y uno de no-datos en el orden de búsqueda. Por el simple hecho de añadir un método `__get__`, un descriptor se pondría por delante de los atributos del diccionario del objeto en el orden de búsqueda. También apuntar que sólo se buscan descriptores entre los atributos de clase, por lo que no tendrá sentido asignar descriptores en otro atributos.

En el caso de la asignación de atributos, se seguirían estos pasos:

1. Se busca descriptores de datos en el diccionario de la clase (`obj.__class__.__dict__`) y todos los diccionarios de las clases padre. Si se encuentra un descriptor de datos, entonces se invoca el método `__set__` del descriptor.

2. Se invoca el método `__setattr__`, si existe, para delegar en él.

3. Como última prioridad, se inserta el atributo en el diccionario del objeto.

En estos pasos no aparecen los descriptores de no-datos. Si realizamos una asignación sobre un descriptor de no-datos, acabaría siendo reemplazado como cualquier atributo normal.


#¿Se puede saltar un descriptor de datos?

La prioridad de los descriptores de datos frente al resto de atributos hace prácticamente imposible *saltárselos* para acceder directamente a un atributo. Todo acceso al atributo pasa por sus manos, regla que se aplica también con el propio descriptor y que da origen a bastantes recursividades sin fin. Por ello es habitual que el descriptor mantenga un atributo auxiliar *"privado"*, ya que de otro modo no tendrá otra forma de acceso directo.

Algo que sí podemos hacer es cambiar las prioridades con la definición de un método `__getattribute__` propio. Como ejemplo, se podría priorizar los atributos del diccionario frente a los descriptores de esta manera:

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

class C(object):
    a12=Descrip(12)
    a200=Descrip(200)
    
    def __init__(self,value):
        self.value=value
        
    def __getattribute__(self, attr):
        dic=super(C,self).__getattribute__("__dict__")
        if attr in dic:
            return dic[attr]
        else:
            return super(C,self).__getattribute__(attr)

c=C(2)

print c.a12  #--> 24  (valor del descriptor)
c.__dict__["a12"]=100
print c.a12  #--> 100 (valor del diccionario)
```


[^1]: En python 2.x, a las clases que derivan de `object` se las denomina *"nuevas clases"* por contraste con las clases que había hasta ese momento. En python 3.x, todas las clases derivarán por defecto de `object`.
