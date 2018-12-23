Title: Clausuras en python - Parte 1
Date: 2013-10-25 21:02
Author: Chema Cortés
Category: Python
Tags: closures
Slug: clausuras-en-python-parte-1

##Funciones Lambda

Antes de ver qué son las **clausuras** (*closures*), veamos
qué tienen las *funciones lambda* que las hacen tan polémicas algunas
veces.

Comencemos con un ejemplo. Te recomiendo que te esfuerces en deducir
cómo funciona sin ir a probar cómo funciona. A continuación te pondré
algunos valores para que elijas los valores de las tres listas:

```python

    i=1
    add_one=lambda x:x+i
	
    lista1=[add_one(i) for i in [0,1,2]]

    i=0
    lista2=[add_one(i) for i in [0,1,2]]

    i=2
    lista3=[add_one(i+1) for i in [0,1,2]]

```

Valores para `lista1`:

1. `[0,1,2]`
2. `[1,2,3]`
3. `[0,2,4]`
4. `[1,3,5]`

Valores para `lista2`:

1. `[0,1,2]`
2. `[1,2,3]`
3. `[0,2,4]`
4. `[1,3,5]`

Valores para `lista3`:

1. `[0,1,2]`
2. `[1,2,3]`
3. `[2,3,4]`
4. `[1,3,5]`

Las soluciones están al final del artículo[^1], pero puedes probarlo
ahora para que lo veas tú mismo.

###¿Qué es lo que ha pasado?

Contrariamente a lo que estamos acostrumbrados con las funciones normales, la
evaluación de una *función lambda* se hace dentro del entorno donde se
ejecuta, independiente del entorno donde se ha definido. Así pués, en la *función lambda* `lambda
x:x+i`, la variable `i` toma el valor de esta variable en el momento
de evaluar la función. Como se usa esta variable para la compresión de la
lista, irá cambiando de valor a medida que se recorre la lista
`[0,1,2]`, por lo que la expresión `add_one(i)` termina convirtiéndose
en la expresión `i+i`, y la expresión `add_one(i+1)` en `i+1+i`.

Tiene un funcionamiento similar a los *macros*, donde se sustituye
*literalmente* la llamada a la función por la expresión equivalente. En
python3, se hace más evidente al denominarse *expresiones lambda* en lugar de *funciones lambda*.

##Clausuras

En una función podemos distinguir dos partes:

- **Código ejecutable**
- **Entorno de evaluación**, más conocido por **Ámbito** o **Scope**

Antes de ejecutar el código de la función, se aumenta el entorno de
evaluación con los *argumentos de entrada* de la función.

Según en qué entorno se evalua la función, tenemos dos ámbitos:

- **Clausura**, también llamado **Ámbito léxico** o **Ámbito
  Estático**, cuando la función se evalua en el entorno donde se ha definido.
- **Ámbito dinámico** cuando se evalua en el entorno donde se invoca la función.

Con esta definición, podemos afirmar que en python las funciones
tienen *ámbito léxico*, con excepción de las funciones lambda que tienen
*ámbito dinámico*.

No voy a considerar las ventajas de uno u otro tipo. Por lo general, las *clausuras*
se consideran mejores para desacoplar el código de la
función del código donde se invoca, lo que ayuda mucho al
mantenimiento y corrección de errores. Es por ello la manera normal de
crear funciones en la mayoría de lenguajes de programación.


###¿Cómo hacer que una función lambda se comporte como si tuviera *clausura*?

La forma de hacer que un función lambda se evalue en el entorno donde
se define consiste en pasar las variables de ese entorno que necesite
en los argumentos de entrada, casi siempre como argumentos por
defecto.

En el ejemplo anterior sería:

```python
    i=1
	add_one=lambda x,i=i:x+i
```

que equivaldrá a

```python
	add_one=lambda x,i=1:x+i
```

En este caso `i` se toma de los argumentos de la función, y tendrá por
defecto el valor de `i` en el momento de la definición de la función
lambda.

No es perfecto, pero es lo mejor que tenemos. Lo recomendable es
evitar las funciones lambda complejas si no queremos llevarnos algunas
sorpresas.

[^1]: Los valores de las listas son las opciones 3, 3 y 4, respectivamente.
