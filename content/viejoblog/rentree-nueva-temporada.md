Title: Rentrée (nueva temporada)
Date: 2011-10-08 18:22
Author: Chema Cortés
Category: Pensamientos
Tags: python, java, jvm, pyday, scala
Slug: rentree-nueva-temporada

Desconectado de mis tareas habituales depués de algunas semanas viajando por Francia, veo que me quedaron varios proyectos y artículos en dique seco que pretendo recuperar. Con la *"reentrada"* (o, como dirían los franceses, *"rentrée"*) me he propuesto algunas metas para esta nueva *temporada* (por llamarla de algún modo) que ahora empiezo.

Junto a los artículos que tengo previstos, intentaré incorporar al blog más comentarios sobre temas técnicos que me vayan surgiendo en el día a día, preferiblemente relacionados con la programación. Sin llegar a la extensión de un artículo, espero que sirvan como gérmen de desarrollos posteriores más extensos.

Como primeras ideas para esta *rentrée*, he tomados dos decisiones: centrar mis desarrollos en la [máquina virtual java][JVM] (plataforma JVM) y aprender a programar con [scala][].

##Máquina Virtual Java (JVM)

Hoy en día, la JVM está omnipresente para casi cualquier dispositivo y sistema operativo. Su uso empresarial es muy extendido, tanto para desarrollo en el lado servidor como para clientes móviles. Librerías y paquetes suficientemente robustos y probados completan una gran plataforma donde desarrollar cualquier tipo de aplicativo que podamos pensar.

Al evaluar la robustez de las librerías java, hay que tener en cuenta que java y su JVM están en constante evolución. El paso de Java5 a Java6 sido muy lento debido a las pocas ventajas que ofrecía el cambio frente al coste de tener que adaptar el código; pero con Java7 se incorpora a la máquina virtual el poder trabajar con tipos dinámicos de datos, lo que mejorará bastante el rendimiento de los lenguajes de scripting como jython, jruby ó groovy, por poner algunos ejemplos. Este cambio parece independizar el desarrollo de la JVM del lenguaje java para pasar a ser una plataforma común para la ejecución de aplicaciones, sea cual sea el lenguaje que se haya usado (objetivo similar a lo que tenía que haber sido .Net).

En lo personal, desde hace mucho tiempo que estoy programando en jython, tal como comenté en otro [artículo][1]. La llegada de los dispositivos android hace aún más interesante la programación para JVM, así como que las numerosas herramientas de software libre que estoy usando estén para esta plataforma. No quiero decir con ésto que renuncie a utilizar la CPython, la máquina virtual *"nativa"* que lleva python, siempre que sea necesario. Tan sólo priorizo la plataforma, JVM, frente a las últimas implementaciones del lenguaje python. Espero que el proyecto [PyPy][] facilite un único camino para el desarrollo del lenguaje, independiente de la máquina virtual empleada.

##Lenguaje Scala

Poco conozco de este lenguaje, la verdad. En el índice [tiobe] de septiembre de 2011 figura en la posición 50, la última posición que entra en valoración. Pero los comentarios que he leído sobre este lenguaje me han picado tanto la curiosidad que he decidido darle un vistazo. Si quieres un consejo: no te limites a un sólo lenguaje de programación. Sólo comparando con otros lenguajes descubrirás las virtudes y limitaciones de los lenguajes que uses. Sobre todo, intenta aprender algún lenguaje *"exótico"*, si por exótico se entiende aquél que no se ve en los estudios oficiales de informática. Siempre que te pidan mostrar tus conocimientos de programador, saber programar en un lenguaje "exótico" será visto como que te entusiasma la programación y que tienes capacidad para aprender cosas nuevas por tu cuenta (Python sigue siendo un excelente ejemplo de lenguaje para estas demostraciones).


Algunas características interesantes de Scala:

- Lenguaje funcional orientado a objeto similar a java, pero superando a éste en simplicidad. Incorpora clausuras y tipado perezoso de datos.
- Escalable (como indica su nombre: **sca**lable **la**nguage)
- Emplea la JVM, aunque también hay versión para .Net. Puede usarse en cualquier sitio que se use java como, por ejemplo, para programación en android.
- Preparado para la programación concurrente. Sigue el modelo "Actor", o lo que es lo mismo, todos los objetos son "actores" con su propio entorno de ejecución.

##Asociacionismo en torno a python

Tangencialmente, he empezado a meterme en la organización de un evento relacionado con python. Creo importante que todos retomemos los contactos personales e intentar hacer reflotar las ilusiones perdidas por esta crisis que estamos viviendo. Si todo va bien, espero vernos en el [Día Python 2011][2] en Zaragoza dentro de la LSWC'11.


*[JVM]: Java Virtual Machine
[1]: {filename}porque-uso-jython.md
[scala]: http://www.scala-lang.org/ "Lenguaje Scala"
[JVM]: http://es.wikipedia.org/wiki/Máquina_virtual_Java
[pypy]: http://pypy.org/ 
[tiobe]:http://www.tiobe.com/index.php/content/paperinfo/tpci/index.html "Índice Tiobe"
[2]: http://python-hispano.org/DiaPythonZGZ
