---
Title: ¿Qué es un coconut?
Date: 2019-04-16 00:00:00
Modified: 2019-04-16 00:51:57
Category: Coconut
Tags: coconut, functional-programming
Slug: que-es-un-coconut
Authors: Chema Cortés
Summary: Inicio de unos artículos dedicados al lenguaje coconut, un lenguaje funcional totalmente *pythónico*, y otras novedades para este nuevo reinicio del blog.
Lang: es
Translation: false
Status:
---

!!! type "...and now for something completely different"

## Python multiparadigma

La primera vez que oí hablar de python allí por finales del siglo pasado, una cosa que me encantó es que se definía como *lenguaje multiparadigma* combinandao el clasicismo de los lenguajes imperativos con la novedosa (entonces) *orientación a objetos* y con algunas características *funcionales* añadidas que lo hacían único. El tiempo ha ido puliendo el lenguaje y la programación funcional se ha ido arrinconando hacia algunos módulos o, directamente, han desaparecido. El propio creador del lenguaje, Guido von Rossum, llegó a pensar en [eliminar todo rastro][1], aunque finalmente sólo desterró la función `reduce` al módulo `functools` alegando que no era una característica que entendiera ni usar un programador python.

Es una pena. La *Programación Imperativa* impuesta como único modo de aprender a programar, sin base para cambiar luego hacia los otros dos paradigmas. Cuando se introdujo la *Programación Orientada a Objetos* con los interfaces gráficos, se empleó mal. Los objetos fueron tamizados por la programación imperativa para verse como sacos de procedimientos que compartían unas mismas variables de estado. La *Programación Funcional*, a pesar de estar presente desde el principio de la historia de la informática, a pesar de ser la que más próxima al pensamiento matemático, quedó fuera del entendimiento de los programadores.

Pero la tendencia se está inviertiendo. Hoy en día es imprescidible la ejecución concurrente, ya sea para aprovechar las CPUs multinúcleo de nuestros dispositivos, ya sea porque necesitamos atender un alto número de peticiones concurrentes. La programación imperativa ya no es apropiada cuando varios hilos de ejecución se acoplan e interfieren entre sí por los mismos recursos. La programación imperativa se hace menos determinista en estos casos y los fallos son imposibles de repetir de una ejecución a otra.

La programación funcional, dentro de lo complejo que sea de entender sus premisas a un programador tradicional, es la única que permite razonar lógicamente sobre la ejecución de un programa concurrente.

## ¿Qué es un coconut?

Python ha avanzando mucho estos años. Es el principal lenguaje usado en ciencia y enseñanza. Los *makers* lo tienen en sus sistemas empotrados como microbit, raspberries pi y similares. Y pronto completará el hito de abandonar la versión 2 para pasar definitivamente a la versión 3, incluyendo entre sus novedades las instrucciones nuevas para la concurrencia y el multiproceso.

Para mi gusto, a python le falta un sistema de tipos más potente y tener características funcionales. Para lo primero, hay avances con el *"tipado gradual"*, soportado por varios IDEs que ayuda mucho en la codificación. Para la programación funcional, python cuenta con algunos módulos como `itertools` y `functools`, pero no deja de ser algo testimonial.

Pero he descubierto un nuevo lenguaje funcional *pythonico*: [coconut][]. Aunque sigo recomendando empezar a programar con un verdadero lenguaje funcional como haskell para evitar adquirir vicios, con coconut se puede tener lo mejor de los dos mundos sin renunciar a usar python.

Me he animado a aprender coconut e ir creando pequeños artículos a medida que vaya aprendiendo. Intentaré hacer comparaciones con otros lenguajes como haskell, scala o typescript, ya que son los otros lenguajes que estoy empleando frecuentemente, además de python.

Sobre el nombre de *coconut* para un lenguaje *pythónico*, hay que recordar que todo lo relativo a *python* proviene de las comedias del grupo humorístico "Monty Python":

{% youtube Fhnjqy8JvEs 500 %}

Pero para los que tenemos ya una edad, *coconut* siempre *serás tú*:

{% youtube xwFp6THEddE 500 %}

[1]: https://www.artima.com/weblogs/viewpost.jsp?thread=98196 "The fate of reduce() in Python 3000"
[coconut]: http://coconut-lang.org/ "Coconut Language"