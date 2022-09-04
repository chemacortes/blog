Title: Lingua Franca
Date: 2012-05-12 17:11
Author: Chema Cortés
Category: Notas
Tags: CompSci, computing science
Slug: lingua-franca

Este mes de mayo, el conocido y muchas veces criticado [índice tiobe][tiobe] comenta que, tras 8 años, las posiciones en este índice de los lenguajes de programación no han sufrido demasiado altibajos, con excepciones notables como el *"Objective C"* empleado por el *ecosistema Apple* (*iPhone/iPad/MacOS*).  Achaca esta inmovilidad a lo costoso de trasladar todo el código base que hemos acumulado de un lenguaje a otro, optando por mantenerse fiel a lenguaje que está utilizando.

Desde mi punto de vista, ésta no es una razón de peso hoy en día. Los distintos lenguajes de programación pueden compartir librerías sin demasiados problemas. Tecnologías como `.Net` o `JVM` facilitan bastante esta tarea, de modo que la mezcla de lenguajes es posible, sin obligar a elegir un único lenguaje al inicio de un desarrollo.

Pienso, por ejemplo, en todos los lenguajes de programación existentes para JVM (groovy, scala, clojure, jython, jruby,...). Todos ellos pueden usar las mismas librerías que usa java, aportando a su vez opciones con las que no cuenta java. Tal vez en esa proliferación de lenguajes alternativos se encuentre la explicación de porqué java ha perdido posiciones con respecto a C++. La evolución de Java se ha quedado algo estancada, tardando demasiado en incorporar características tan demandadas como las *"clausuras"* o *tipos dinámicos* que ofrecen los otros lenguajes.[^1]

Porque es la evolución de los lenguajes de programación lo que realmente es interesante. No hace muchos años, creo que en la revista DrDobb's, existía una sección fija dedicada al *"lenguaje exótico del mes"* que pretendía mostrar lenguajes más expresivos, muchos de dominio específico orientados a resolver problemas concretos, pero donde a veces se veían pequeñas joyas como el APL. Los lenguajes de uso habitual se consideraban limitados, y muchas veces la evolución en los algoritmos fallaba en el preciso momento de tener que codificarlo en un programa de ordenador. El lenguaje máquina dejó paso a otros modo de entenderse con la máquina.

Con el tiempo, cuando la programación se convirtió en ciencia, aparecieron los **"paradigmas"** y las **"metodologías"**. La programación se volvió bastante más abstracta y la ingeniería impuso sus reglas de eficiencia que terminó por relegar los lenguajes de programación a un segundo plano. La *"expresividad"* se conseguía ahora mediante herramientas CASE e IDEs inteligentes que imponían sus lenguajes de programación.

Estamos en una época que poco va a cambiar en cuanto a lenguajes, tal como afirma [Tiobe][tiobe]. La razón de peso son las herramientas que usamos, que no las librerías. Los lenguajes más populares (los que aparecen en el índice tiobe) poseen un proceso evolutivo por el que adaptan los aciertos de los otros y se desprenden de lo obsoleto. No aumenta el número de lenguajes, pero las versiones de los lenguajes aumentan sin parar. Una estrategia evolutiva en el más amplio sentido que hace que los lenguajes se parezcan cada vez más entre sí, con formas muy similares para resolver los mismo problemas que llamamos "patrones de diseño" y concepciones similares.

¿El inicio de una *"Lingua Franca"*?



[tiobe]: http://www.tiobe.com/index.php/content/paperinfo/tpci/index.html "TIOBE Programming Community Index"
[^1]: En la literatura, se suele mencionar al lenguaje Scala como "lo que debería haber sido la evolución de Java".
