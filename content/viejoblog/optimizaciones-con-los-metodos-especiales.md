Title: Optimizaciones con los Métodos Especiales
Date: 2011-06-24 00:51
Author: Chema Cortés
Category: Python
Tags: técnicas dinámicas
Slug: optimizaciones-con-los-metodos-especiales

#Métodos Especiales

Dentro del llamado ["modelo de datos"][modeldata] de python, la [*sobrecarga de operadores*][2], tan característica de la programación orientada a objetos, se realiza mediante la definición de algunos métodos de [nombre especial][1]. A través de esta técnica se define cómo se comportará una clase frente a los operadores del lenguaje.

Estos métodos especiales son invocados *implícitamente* por el intérprete para realizar la operación, decidiendo en tiempo de ejecución cuáles de los  métodos serán más adecuados para realizar la operación.

Por ejemplo, el método especial `__nonzero__` determina el valor `True` o `False` de la instancia, útil para expresiones condicionales. De no estar definido este método, se considera el método `__len__` (usado por la función `len()`) para determinar como `False` si tiene tamaño cero. En caso de que tampoco cuente con este método, se considera siempre como `True`.

Al ser parte intrínseca del lengueje, estos *métodos especiales* inciden seriamente en redimiento del intérprete. Con sólo definir el método especial `__getattribute__`, por ejemplo, encargado de controlar todo acceso a los atributos de un objeto, la sobrecarga del intérprete se volvería pesada y lenta sin posibilidad de mejorar mucho mediante rutinas en lenguaje C. Para evitar este impacto negativo, se toman algunas *"optimizaciones"* que sólo son aplicables a los métodos especiales.

#Optimizaciones de Métodos Especiales

Con los *"Métodos Especiales"* se dan dos optimizaciones en la invocación "implícita" de un método especial:

1. Implícitamente, sólo se buscará métodos especiales en la clase, ***nunca*** en el diccionario del objeto.

2. Implícitamente, ***nunca*** se accederá a un método especial a través de `__getattribute__`

Estas dos optimizaciones (más bien *"atajos*") son origen de muchos errores y malas interpretaciones, responsable en primera instancia de que determinado código no funcione como se esperaba en teoría.

Recalcar que estas optimizaciones sólo ocurren en las invocaciones *"implícitas"*. Si hacemos la invocación explícita a través del nombre especial del método entonces se sigue el procedimiento estándar de búsqueda de atributos.

Veamos algunos ejemplos y contraejemplos:

```
>>> class C(object):
...     def __len__(self):
...         return 5
... 
>>> obj=C()
>>> len(obj)
5
>>> 
>>> obj.__len__=lambda:100
>>> len(obj)
5
>>> obj.__len__()
100
```

La clase responde a la función estándar `len()` a través del método `__len__`. Como se ve, aunque cambiemos el método en el diccionario del objeto, la función `len()` sigue usando el método especial de la clase. Si se invoca el método *explícitamente* (`obj.__len__()`), entonces sí que se usará el método del diccionario del objeto.

Primera conclusión:
>Para que funcione correctamente, toda *técnica dinámica* que involucre métodos especiales ha de actuar sobre la clase.

Estudiemos otro ejemplo:

```python
class C(object):

    a=100

    def __getattribute__(self, attr):
        value=super(C,self).__getattribute__(attr)
        print "Desde C # '%r'.'%s'==%r"%(self,attr,value)
        return value
```
```
>>> obj=C()
>>> obj.a
Desde C # '<__main__.C object at 0xb77d4b2c>'.'a'==100
100
>>> C.a
100
```

En la prueba, accedemos al atributo `a` a través de la instancia `obj` y a través de la clase `C`. En el primer caso, se llama a `__getattribute__` para acceder al atributo; mientras que en el segundo no lo hace. Muy a menudo se piensa errónemente que la clase usa implícitamente sus propios métodos especiales y no es así.

Como objeto que es, una clase también es una instancia. A la clase de una clase la denominaremos **"metaclase"**[^2] y tendrá como ancestro superior la clase `type` (del mismo modo que toda clase tenía como ancestro la clase `object`)[^1]. Es a esta metaclase donde se buscan los métodos especiales de la propia clase:

```python
class Meta(type):
    def __getattribute__(cls, attr):
        value=super(Meta,cls).__getattribute__(attr)
        print "Desde Meta# '%r'.'%s'==%r"%(cls,attr,value)
        return value

class C(object):

    __metaclass__=Meta

    a=100

    def __getattribute__(self, attr):
        value=super(C,self).__getattribute__(attr)
        print "Desde C # '%r'.'%s'==%r"%(self,attr,value)
        return value
```

De donde podemos sacar la segunda conclusión:

>Los métodos especiales que operen con clases deberán ir en la metaclase.

Haciendo un fundido de los ejemplos anteriores:

```python
class Meta(type):
    def __getattribute__(cls, attr):
        value=super(Meta,cls).__getattribute__(attr)
        print "Desde Meta# '%r'.'%s'==%r"%(cls,attr,value)
        return value
    
    def __len__(cls):
        return 999

class C(object):

    __metaclass__=Meta

    def __getattribute__(self, attr):
        value=super(C,self).__getattribute__(attr)
        print "Desde C # '%r'.'%s'==%r"%(self,attr,value)
        return value

    def __len__(self):
        return 100
```

Con este código, se puede comprobar las siguientes formas de invocar `__len__` para la instancia:

```
>>> obj=C()
>>> len(obj)
100
>>> len(C)
999
```

Aquí observamos que la llamada *implícita* a `__len__` se salta el `__getattribute__` tanto de la clase como de la metaclase como ya estaba anunciado. 

Analicemos algunas llamadas *explícitas* (recomiendo ir probándolas):

- vía la instancia `obj.__len__()`:  se usará el `__getattribute__` de la clase para buscar el método `__len__`
- vía el tipo `type(obj).__len__(obj)`:   se usará el `__getattribute__` de la metaclase para buscar el método `__len__`. Por orden de prioridad, se usará el `__len__` de la clase.
- vía la metaclase `type(C).__len__(C)` se usará el `__getattribute__` de `type`, invocando finalmente el `__len__` de la metaclase

En el orden de búsqueda, tiene prioridad el método `__len__` definido en la clase frente al definido en la metaclase. Por ese motivo no puede emplearse la llamada explícita `C.__len__()` ya que no corresponde con un método de clase.

#Conclusión

Entendiendo cómo funcionan estas optimizaciones vistas con los *métodos especiales*, y con bastante cuidado, será posible hacer que nuestras clases se comporten según lo esperado en las operaciones normales. Una buena planificación de nuestro modelo de datos según lo que espera el intérprete conseguirá que nuestro código sea más legible y fácil de mantener.

[modeldata]: http://www.python.org/doc//current/reference/datamodel.html "Modelo de datos"
[1]: http://www.python.org/doc//current/reference/datamodel.html#special-method-names "Nombres especiales de métodos"
[2]: http://es.wikipedia.org/wiki/Sobrecarga "Sobrecarga de operadores"

[^1]: Siguiendo con la relaciones entre clases y objetos, la clase `type` es a la vez instancia de `type` y subclase de `object`.
[^2]: En próximos artículos veremos el funcionamiento de las *metaclases*
