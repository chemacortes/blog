---
Title: Coconut - Primeros pasos
Date: 2019-05-02 01:20:16
Modified: 2019-05-02 23:58:10
Category: Coconut
Tags: coconut, functional-programming, python
Slug:
Authors: Chema Cortés
Summary: Primera toma de contacto con el lenguaje coconut, su instalación y detalles a tener en cuenta con la compatibilidad con las versiones de python utilizadas.
Lang: es
Translation: false
Status:
---

[Coconut][1] es un lenguaje funcional completamente *pythónico*. Otro modo de hacer las cosas en python. Al principio puede parecer muy distinto, pero a medida que se conoce te das cuenta de lo útil que es a veces abordar ciertos problemas desde un punto de vista *puramente funcional*.

## Qué versión de python utilizar

Antes de empezar con *coconut*, una advertencia sobre las versiones de python. Para su ejecución, el código *coconut* se traduce en código python, pudiendo elegir qué versión de python ejecutará el código final. Se puede elegir [varias versiones de python][2] objetivo, independientemente de la versión de python con la que estemos trabajando. Por defecto, se genera *"código universal"*, válido para todas las versiones de python. Emplear este *código universal* requiere renunciar a algunas características de *python 3* que no tienen equivalencia en *python 2* como es la notación de tipos, el operador `'@'` para multiplicación de matrices o las sentencias `async` y `await` para programación asíncrona.

En esta serie de artículos sobre *coconut* voy a trabajar siempre con una instalación de *python 3*, lo recomendado para nuevos proyectos. Así mismo, el código generado se ejecutará en *python 3*. Pero transpilar a *código universal* debería ser igualmente válido en la mayoría de casos. Es más, ya que todo código *python 3* es código válido en *coconut*, se podría emplear para convertir código de *python 3* a *python 2*, aunque no lo recomiendo.

En la documentación tienes [información sobre compatibilidad][3] de *coconut* con algunas versiones de python.

[1]: http://coconut-lang.org/ "Coconut language"
[2]: https://coconut.readthedocs.io/en/master/DOCS.html#allowable-targets
[3]: https://coconut.readthedocs.io/en/master/DOCS.html#compatible-python-versions

## Instalación de coconut

Para instalar *coconut* mi forma preferida es usar `conda` empleando el canal `conda-forge`. Siempre es recomendable crear un entorno virtual donde aislar las dependencias del resto de nuestra instalación. En concreto, la instalación de *coconut* incluye varios kernels de jupyter y una configuración de pygments para el coloreado de sintáxis.

En particular, prefiero crear un fichero de entorno (`environment.yml`) que determine las dependencias, tanto las que instala conda, como las que se necesite instalar con pip. Podríamos concretar con precisión las versiones que vamos a usar; pero me voy a limitar a las dependencias mínimas para la versión que estoy usando ahora, *coconut 1.4.0*.

{% include_code 2019Q2/environment.yml lang:yaml :hidefilename: Entorno virtual 'coco' %}

Se fija la versión de `python=3.6` ya que ésta es la versión superior recomendada para *coconut*. Posiblemente también funcione correctamente con `python=3.7`.

Entre las dependencias encontramos:

- **pygments**: facilitará el coloreado de sintáxis de código *coconut*
- **watchdog**: chequea de cambios en ficheros para automatizar recompilaciones
- **pyparsing**/**cpyparsing**: *parseo* de texto, utilizado por el traspilador y el interface de línea de comandos. Se fija la versión de `pyparsing=2.2.0` ya que daba algunos fallos dentro de `jupyter console` con versiones superiores[^1].

`cPyparsing` es una versión optimizada de `pyparsing`. Su instalación necesita los compiladores de C apropiados para la creación módulos python para el sistema. Con linux, el entorno que uso, no hay problema; pero es posible que en windows dé errores por no encontrar el compilador MS C++. Si no sabes cómo se instala, siempre puedes quitar `cpyparsing` del fichero `environment.yml` para que siga usando `pyparsing`.

Dado que *coconut* es un desarrollo muy activo, también recomiendo la instalación de una versión de desarrollo de *coconut*. Muchas veces, los problemas encontrados pueden estar resueltos en desarrollo. Pero siempre es interesante probar las novedades que se van a añadiendo y nunca está de más animarse a contribuir en posibles mejoras.

El entorno de desarrollo estará definio así:

{% include_code 2019Q2/environment-dev.yml lang:yaml :hidefilename: Entorno virtual 'cocodev' %}

La instalación de *coconut* y sus dependencias para este entorno se delega totalmente en pip. Se añade el módulo `coconut-prelude` que nos facilita un mecanismo similar al `Prelude` de haskell para tener un entorno configurado con las funciones más habituales en programación funcional.

Con estos dos ficheros, se crean los entornos virtuales:

~~~.plain
$ conda env create -f environment.yml
...
$ conda env create -f environment-dev.yml
...
~~~

## Primer contacto: Hola Mundo

Para ejecutar coconut, se debe activar primero el entorno:

~~~.plain
$ conda activate coco
$ coconut
Coconut Interpreter:
(type 'exit()' or press Ctrl-D to end)
>>>
~~~

Sale una interface de línea de comando similar a la que tiene python, incluso se puede introducir código python normal:

~~~.coco
>>> print("¡Hola, Mundo!")
¡Hola, Mundo!
~~~

En *coconut*, éste sería nuestro *"Hola Mundo"*:

~~~.coco
>>> "¡Hola, Mundo!" |> print
¡Hola, Mundo!
~~~

El operador `|>` puede verse como un *pipe* que encadena operaciones, una tras otra, que será de uso común. Se puede describir como una *"aplicación del resultado de la izquierda en la expresión de la derecha"*.

Por poner ejemplos de aplicaciones en cadena:

~~~.coco
>>> "¡Hola, Mundo!" |> len |> print
13
>>> "¡Hola, Mundo!" |> list |> print
['¡', 'H', 'o', 'l', 'a', ',', ' ', 'M', 'u', 'n', 'd', 'o', '!']
>>> "¡Hola, Mundo!" |> print |> print
¡Hola, Mundo!
None
~~~

Probemos la ejecución de ficheros. Los ficheros de *coconut* tienen por extensión `.coco`. Creemos un fichero `hola.coco` con una única línea:

~~~.coco
"¡Hola, Mundo!" |> print
~~~

Para ejecutarlo:

~~~.plain
$ coconut --run hola.coco
Compiling         hola.coco ...
Compiled to       hola.py .
¡Hola, Mundo!
~~~

De la *transpilación* se obtiene el fichero `hola.py`, que es el que se usa en la ejecución. Se podría volver a ejecutar sin intervención de *coconut*:

~~~.plain
$ python hola.py
¡Hola, Mundo!
~~~

## Factorial en coconut

Como obsesión de este blog está la comparación de formas de hacer el cálculo del factorial. Recomiendo seguir el [tutorial de coconut][4] donde se detalla, paso a paso, cómo ir cambiando la formulación de factorial desde estructuras imperativas a funcionales.

Una formulación simple podría ser esta:

~~~.coco
def product(lst: int[]) -> int = reduce((*), lst)
def factorial(n: int) -> int = range(2, n+1) |> product

10000 |> factorial |> print
~~~

Aunque las veremos con detalle más adelante, aquí adelantamos varias características de *coconut*:

- Una función puede devolver una expresión, similar a las funciones *lambda*
- La función `reduce` está disponible por defecto (importante en programación funcional)
- Se usa el operador multiplicación como `(*)` (*al estilo haskell*) sin necesidar de importarlo del módulo `operator`
- Se usa una notación de tipos extendida con `int[]` para hacer referencia a una *lista de enteros*.

La *notación de tipos* es en realidad parte de *python 3*, lo único que hace *coconut* es facilitar su uso con una notación extendida.

Si es la primera vez que ves *programación funcional*, seguramente no entiendas nada. Pronto tendrá todo sentido y te empezarás a preguntar porqué no la conocistes antes.

[4]: https://coconut.readthedocs.io/en/master/HELP.html "Tutorial de coconut"

[^1]: Este problema también lo tiene la instalación de coconut para **python 2**. En este caso, la simple ejecución del interface de línea de comando sobra para entrar en un bucle sin fin que agote rápidamente la memoria y bloquee todo el equipo. Forzar la versión a `pyparsing=2.2.0` solventa el problema.
