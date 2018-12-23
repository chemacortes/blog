Title: Descriptores - Parte 3
Date: 2012-06-05 00:37
Author: Chema Cortés
Category: Python
Tags: descriptor, técnicas dinámicas
Slug: descriptores-parte-3

Hasta ahora hemos visto cómo funcionan los *descriptores* para acceder a atributos de datos que funcionan como *"propiedades"* (`property`). Pero al iniciar esta serie de artículos dije que los *descriptores* son también *"los responsables del funcionamiento de  métodos, métodos estáticos, métodos de clase y del mecanismo `super()` responsable de la herencia múltiple"*.  Es el momento de ver cómo lo hacen:

## Métodos vistos como funciones

Es común pensar que los métodos y las funciones comparten muchas similitudes. Considerando que en python las funciones son [objetos de primera clase][1]  lo primero que podemos probar es a asignar directamente funciones a atributos de una clase para crear métodos *dinámicamente*:

```python
class C(object):
    pass

def func(obj):
    print "obj is %s " % obj

C.method = func

#prueba del nuevo método
c = C()

c.method()    # cualquiera de...
C.method(c)   # ...estas invocaciones...
func(c)       # ...dan el mismo resultado
```

Esta *dualidad* entre funciones y métodos va más allá si observamos que, en realidad, las funciones son *"descriptores"*, tal como podemos comprobar mirando su diccionario:

```python
>>> hasattr(func, "__get__")
True
>>> hasattr(func,"__set__")
False
```

Concretamente, las funciones son *"descriptores de no-datos"* y como tales se aplicarán las reglas comentadas en artículos previos. En concreto, se buscarán antes los métodos en el diccionario del objeto que entre los atributos de su clase[^1], lo que nos va a permitir suplantar métodos en tiempo de ejecución.

Con añadir funciones a los atributos de clase será suficiente para la mayoría de casos que nos podamos enfrentar. El resto de este artículo va orientado para algunos casos de *"técnicas dinámicas"* que requieren diferenciar el comportamiento de un objeto respecto al resto de las instancias de la misma clase.

## Invocación de descriptores y sus enlaces

Hasta ahora no nos habíamos preocupado por el segundo argumento que se pasa al método `__get__` en el interface "descriptor", al que se denomina "propietario" (*"owner"*) y que siempre coincide con la clase de la instancia. A través de la instancia o del propietario, `__get__` devolverá el atributo enlazado con la instancia y/o clase según sea el comportamiento buscado.

Veamos cómo funciona en detalle: supongamos que tenemos una instancia `obj` de una clase `Cls` y accedemos a través del descriptor `desc`. Tendremos las siguientes formas de establecer el enlace:

- **Llamada directa**: `__get__(obj)` invocación explícita a partir del descriptor. Es la más simple, aunque infrecuente. (pe: `desc.__get__(obj)`)

- **Enlace con la Instancia**: `__get__(obj, Cls)` Se usa en el acceso al atributo `obj.desc`, donde se efectúa la llamada implícita `Cls.__dict__['desc'].__get__(obj, Cls)`

- **Enlace con la clase**: `__get__(None, Cls)` Se usa en el acceso al atributo `Cls.desc`, donde se efectúa la llamada implícita `Cls.__dict__['desc'].__get__(None, Cls)`

- **Enlace con _super_**:  se da con instancias de la clase `super` utilizadas en la herencia múltiple. El acceso al atributo `super(Cls, obj).desc` inicia una búsqueda en `obj.__class__.__mro__` para encontrar la clase base inmediatamente precedente a la clase `Cls` (=`SuperCls`) e invoca el descriptor con la llamada `SuperCls.__dict__['desc'].__get__(obj,  obj.__class__)` con lo que obtenemos el atributo enlazado con una de las clase  padre según el algoritmo [MRO][].

Como se puede observar, el método `__get__` del descriptor recibe diferentes argumentos según el enlace que se vaya a usar, lo que nos permitirá programar el descriptor según el uso que deseemos darle.

## Técnicas dinámicas

Para realizar nuestros experimentos, supongamos que tenemos el siguiente descriptor:

```python
def desc(*args, **kwargs):
    print args, kwargs
```

Es una simple función que imprime los argumentos que recibe con el fin de poder analizarlos. Con una clase y una instancia intentaremos ver cómo añadirles métodos dinámicos:

```python
class Cls(object):
    pass

obj=Cls()
```

El caso trivial es añadir el descriptor como atributo de la clase:

```python
>>> Cls.meth=desc
>>> obj.meth
<bound method Cls.desc of <__main__.Cls object at 0x8ffd3ac>>
>>> obj.meth()
(<__main__.Cls object at 0x8ffd3ac>,) {}
```

Encaja con el funcionamiento estándar de los descriptores, que pasa por establecer primero un enlace del descriptor con la instancia o con la clase para obtener después el método ejecutable.

Pero a veces necesitamos añadir métodos sobre la instancia y no sobre la clase. Ésto puede ser debido a:

1. Sólo queremos modificar una instancia sin que afecte al resto
2. Queremos *"decorar"* el método de clase a través de un método de la instancia

Técnicamente, son los llamados **"métodos singleton"** que lenguajes como [ruby][2] incluyen en su sintaxis, pero que en python se implementan hackeando los descriptores.

Si añadiésemos un descriptor a una instancia sin establer ningún enlace:

```python
>>> obj.meth=desc
>>> obj.meth()
() {}
>>> obj.meth
<function desc at 0xb76776bc>
```

Vemos que el funcionamiento es similar a si hubiéramos ejecutado directamente la función. En realidad, actúa como **"métodos estáticos"**, descriptores que no están enlazados con nada.

Para conseguir que el descriptor funcione como un método normal, necesitamos enlazarlo con la instancia:

```python
>>> obj.meth=desc.__get__(obj, Cls)
>>> obj.meth()
(<__main__.Cls object at 0xb767adec>,) {}
>>> obj.meth
<bound method Cls.desc of <__main__.Cls object at 0xb767adec>>
```

Aquí ya vemos que el método se identifica como un **"método normal"** más de la clase `Cls`.

De forma parecida, podríamos enlazar el descriptor con la clase, pero vista como instancia, no como clase, con lo que obtenemos un **"método de clase"**:

```python
>>> obj.meth=desc.__get__(Cls, type(Cls))
>>> obj.meth()
(<class '__main__.Cls'>,) {}
```


Hemos visto las opciones posibles para realizar diversas técnicas dinámicas. No es habitual verlas en el código que usamos normalmente. Casi puedo asegurar que si necesitas alguna de estas técnicas, es que te has pasado por alto alguna otra forma más sencilla de hacer lo mismo.


##Pequeño truco

Todo lo anteriormente dicho funciona siempre que estemos trabajando con *"descriptores de no-datos"*. Si deseamos que un método de la clase no sea suplantado por un método en la instancia basta con crearlo como *"descriptor de datos"*. Lo más sencillo es usar el decorador `@property`:

```python
>>> class Cls(object):
...  @property
...  def meth(self):
...    print "Desde clase"
... 
>>> obj=Cls()
>>> obj.meth=desc.__get__(obj,Cls)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: can't set attribute
```



[1]: http://en.wikipedia.org/wiki/First-class_object
[2]: http://www.ruby-doc.org/docs/ruby-doc-bundle/UsersGuide/rg/singletonmethods.html "Singleton methods in Ruby"
[mro]: http://cafepy.com/article/python_attributes_and_methods/ch02s04.html "Artículo recomendable sobre el algoritmo MRO"
[^1]: Este orden no se respeta con los *"métodos especiales"* y cuando estamos trabajando con *"descriptores de datos"*. Revisar el resto de artículos sobre descriptores.


##Resto de artículos de la serie
1. [Optimizaciones con los Métodos Especiales]({filename}optimizaciones-con-los-metodos-especiales.md)
2. [Método \_\_getattribute\_\_]({filename}metodo-__getattribute__.md)
3. [Descriptores – Parte 1]({filename}descriptores-parte-1.md)
4. [Descriptores – Parte 2]({filename}descriptores-parte-2.md)

##Descriptor Howto
Como referencias en la documentación oficial:

1. [Descriptor HowTo Guide](http://docs.python.org/howto/descriptor.html)
2. [Implementing Descriptors](http://docs.python.org/release/3.1.5/reference/datamodel.html#implementing-descriptors)
