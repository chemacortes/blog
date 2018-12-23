Title: Método __getattribute__
Date: 2011-06-26 18:59
Author: Chema Cortés
Category: Python
Tags: técnicas dinámicas
Slug: metodo-__getattribute__

Si has seguido hasta ahora la serie de [artículos sobre descriptores][1], habrás visto que buena parte de la *magia* de los objetos en python se debe al método `__getattribute__` que todo objeto adquiere de su antecesor común, la clase `object`.

En el último artículo, donde hablaba de las [optimizaciones de los métodos especiales][2], también comentaba algunas optimizaciones que tenían qué ver con el método `__getattribute__` y proponía un ejercicio:

>¿Sabrías qué es lo que pasa en el siguiente caso? ¿Se invoca el método __getattribute__ en algún momento? ¿Sería una llamada implícita o explícita?

>        obj.__getattribute__("__getattribute__")

Quien se enfrenta a este código por primera vez, lo primero que piensa es que se va a producir una *autorecursividad* puesto que en el acceso al método `__getattribute__` se debería invocar el propio método `__getattribute__` y así indefinidamente.

Si embargo, cuando se prueba se ve que funciona tal y como se espera. Entonces, ¿cómo se evita la recursividad?

En el artículo de [optimizaciones de los métodos especiales][2] hablábamos de dos optimizaciones (*atajos*) de las llamadas *implícitas* a métodos especiales:

1. Implícitamente, sólo se buscará métodos especiales en la clase, ***nunca*** en el diccionario del objeto.

2. Implícitamente, ***nunca*** se accederá a un método especial a través de `__getattribute__`

La intuición nos dice que aquí está la respuesta de que no tengamos *autorecursividad*.

Antes de analizar lo que está pasando, señalar que en el acceso a atributos se usa el operador '`.`' (*punto*) que, como cualquier otro operador, está sujeto a las mismas optimizaciones que hemos apuntado. Para su labor, el operador `.` empleará el método especial `__getattribute__`.

La invocación `obj.__getattribute__("atributo")` se produce en dos pasos:

1. *Implícitamente*, el operador '`.`' accede directamente al método `__getattribute__`, aplicando las optimizaciones.
2. Se invoca *explícitamente* a `__getattribute__` para que retorne el valor del `"atributo"`

Así pues, el resultado final consiste en la combinación de una llamada implícita y otra explícita.

Como corolario, se puede afirmar que "Nunca se invocará a `__getattribute__` para acceder a `__getattribute__`". No será la primera vez que alguien lo haya intentado.


[1]: {tag}descriptor "Artículos sobre descriptores"
[2]: {filename}optimizaciones-con-los-metodos-especiales.md "Optimizaciones con los Métodos Especiales"
