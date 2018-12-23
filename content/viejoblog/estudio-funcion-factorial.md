Title: Estudio función factorial
Date: 2011-06-06 01:22
Author: Chema Cortés
Category: Python
Tags: algorithm, factorial, maths
Slug: estudio-funcion-factorial

Hace un tiempo me dió por recopilar distintas funciones en python para calcular el [factorial][1]. Aquí van todas, algunas bastante curiosas. Si conoces algún tipo más, no dejes de añadirla en los comentarios.

[1]: http://es.wikipedia.org/wiki/Factorial

#Versión recursiva

Todo programador ha tenido que ver esta definición como ejemplo de funciones recursivas :

```python
def fact(n):
    if n==0:
        return 1
    else:
        return n*fact(n-1)
```


Se podría hacer algo más compacta usando el operador ternario:

```python
def fact(n):
    return 1 if n==0 else n*fact(n-1)
```

Como toda función recursiva en python, existe el peligro de que nunca termine la función. Es el motivo por el que python tiene fijado un límite de recursividad dado por `sys.getrecursionlimit()`, que por defecto es de `1000` invocaciones recursivas o, lo que es lo mismo, que no podamos calcular factoriales mayores de 1000.

Podemos incrementar el límite con `sys.setrecursionlimit(n)`, pero seguirá siendo una solución provisional. Lo mejor es pasarnos a una solución *"iterativa"*.


#Versión iterativa

También es una de la funciones más conocidas por todo programador:

```python
def fact(n):
    res=1
    for i in xrange(1,n+1):
        res*=n
    return res
```

Normalmente, todo lenguaje tiene un límite en el tamaño de un entero que hace que esta función no pueda calcular factoriales muy grandes. Pero python tiene la característica de pasar de *entero* a *entero largo* cuando así lo requiera la operación, lo que hace que se puede calcular cualquier número factorial, con el único límite de tiempo para calcularlo. Por lo general, con número grandes cuesta menos calcular el factorial que imprimirlos en pantalla.


#Versión aproximada (función de Stirling)

Para número muy grandes, existe una aproximación llamada ["Aproximación de Stirling"][2] que se suele usar en *mecánica estadística*.

[2]: http://es.wikipedia.org/wiki/F%C3%B3rmula_de_Stirling

```python
import math
def fact(n):
    return math.sqrt(2*math.pi*n)*math.pow(n/math.e,n)
```

Lamentablemente, los números reales (tipo `double`) son aquí una limitación de tamaño, por lo que no podemos hacer cálculos para números altos (precisamente, para los que teóricamente iba mejor esta función).


#Versiones one-line

Muchas veces, los programadores se toman como reto poder expresar una fórmula compleja en una sóla línea, de modo que se pueda sustituir la llamada a la función por la definición de esta directamente. Son las llamadas *funciones "oneline"*.

```python
reduce(lambda x,y:x*y,xrange(1,n+1),1)
```

Podemos aprovechar que tenemos el operador multiplicación y con ello evitar la función `lambda` (últimamente, en desuso):

```python
import operator
reduce(operator.mul, xrange(1,n+1),1)
```

Algo más bizarro, evitando `lambda` y `reduce`:

```python
[j for j in [1] for i in range(2,n+1) for j in [j*i]][-1]
```

Esta versión es en realidad un *"reduce sin usar reduce"*. Para entender cómo funciona, lo mejor es verlo como varios `fors` anidados:

```python
def fact(n):
    for j in [1]:
        for i in range(2,n+1):
            for j in [j*i]:
                yield j

res=list(fact(n))[-1]

```

El primer `for` tan sólo sirve para dar una valor inicial a la variable `j`, y el tercer `for` sería el equivalente *"oneline"* de `j=j*i`.

En realidad, esta función no está muy optimizada ya que mantiene en memoria la lista completa de todos los resultados intermedios. Un modo más inteligente de usar esta expresión sería como un iterador, donde los resultados intermedios ya no son almacenados:

```python
for res in (j for j in [1] for i in range(2,n+1) for j in [j*i]):
    pass
```

Aunque funciona perfectamente, no se puede considerar como función de una sóla línea. Para conseguirlo, tenemos que ir a algo totalmente críptico, incluyendo `reduce` y `lambda`, que acabaría siendo el siguiente engendro:

```python
reduce(lambda x,y:y,(j for j in [1] for i in range(2,n+1) for j in [j*i]))
```

¿Se os ocurren otras formas de expresar el factorial en una sóla línea?
