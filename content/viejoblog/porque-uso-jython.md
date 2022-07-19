---
Title: Porqué uso jython
Date: 2011-05-30 19:04
Modified: 2022-07-19 20:58:17
Author: Chema Cortés
Category: Python
Tags: glassfish, h2, jdbc, jython, zxjdbc
Slug: porque-uso-jython
Status: hidden
---

# Python de sabores

Cuando hablamos de **python**, normalmente nos referimos a su versión _canónica_ implementada en lenguaje C, también conocida por _"CPython"_. Toda la evolución del lenguaje se realiza alrededor de esta implementación y pocas veces se piensa en otras implementaciones. Pero una de las características de python es ser multiplaforma, y lo demuestra con implementaciones para varias plataformas. Algunas de las implementaciones más interesantes serían:

- [Jython][]:
  Implementación para JVM que se integra y hace uso de la numerosísismas
  librerías Java y entornos J2EE. Combina un entorno robusto que rodea a Java con la programación dinámica de python.

- [IronPython][]:
  Una de las implementaciones para la plataforma .Net y mono. Se integra
  con el _framework_ .Net de Microsoft, llegando a una eficiencia bastante
  cercana al lenguaje C#.

- [PyPy][]:
  Un python escrito en python. Su objetivo es librar a python de las
  limitaciones impuestas por el lenguaje C, dando lugar a una implementación
  puramente python.

Cada una de estas implementaciones lleva su propio ritmo de desarrollo, siguiendo la estela de _CPython_. En estos momentos, el lenguaje python (CPython) está parado debido a la moratoria [PEP-3003][] de dos años, a punto de terminar, que se está aprovechando para acercar a CPython el resto de implementaciones y así unir las distintas comunidades de desarrolladores en el siguiente avance de Python hacia la versión 3.

[jython]: http://jython.org
[ironpython]: http://www.codeplex.com/Wiki/View.aspx?ProjectName=IronPython
[pypy]: http://www.python.org/dev/peps/pep-3146/#pypy
[pep-3003]: http://www.python.org/dev/peps/pep-3003/

# Python con sabor Java

De entre todas la implementaciones de python, la que uso habitualmente en mi trabajo es [jython][]. Sin entrar en polémicas sobre si un lenguaje es mejor que otro, cuando uno se decide por un lenguaje _híbrido_ como jython lo hace desde el convencimiento de que la mejor solución consiste en usar lo bueno de ambos mundos. Por un lado, los entornos java ofrecen robustez y librerías bien probadas para cualquier aplicación empresarial; por otro lado, jython ofrece técnicas de programación dinámica que mejoran la productividad.

Entrando en detalle, este sería un listado de ventajas e incovenientes de usar jython sobre python y/o java:

## Multiplataforma

Aunque python ya venga instalado en prácticamente todo sistema linux o macintosh, o incluso aparezca empotrado en aplicaciones como openoffice/libreoffice, no siempre es posible controlar qué versiones, módulos y librerías hay instalados en el sistema. La disparidad de sistemas y configuraciones hace inviable contar con un entorno homogéno para ejecutar nuestro programa python. Por lo general se desarrolla con una configuración fijada, con la esperanza de que el sistema de producción cuente con la misma configuración.

Jython se aprovecha la difusión de la máquina virtual JVM en casi todos los sistemas. Esta máquina virtual nos crea una capa de abstracción que facilita el traslado de la misma configuración de nuestro entorno de desarrollo al sistema de producción, tan fácil como copiar un fichero de un sistema a otro.

Además resulta sencillo crear un entorno jython _portable_[^1] en un pendrive o un disco duro externo, con lo que podemos llevarnos nuestro entorno de desarrollo con nosotros.

## Velocidad y memoria

Existe cierta idea equivocada que los programas java son lentos y consumen mucha memoria. En realidad, java se inventó para sistemas empotrados, como demostraría las aplicaciones y juegos para existen para teléfonos móviles. Hoy en día, una aplicación para java es bastante rápida una vez arrancada la máquina virtual, y el consumo de memoria puede delimitarse para no agobiar al resto del sistema.

Así mismo, el aspecto gráfico de las aplicaciones java es muy similar a las aplicaciones nativas, disponiendo de interfaces de bajo nivel para control gráficos y dispositivos de entrada y salida.

## Sincronismo multihilo

Con el tiempo, la gestión de los hilos de ejecución en una máquina virtual JVM ha llegado a superar cualquier otra implementación gracias a la capa de abstracción que impone. En C, es una labor del programador realizar esta gestión a mano o, con algo de suerte, disponga de alguna librería que facilite el sistema operativo donde se vaya a ejecutar la aplicación, no consiguiendo toda la estabilidad que sería deseable (un ejemplo sería la inestabilidad de algunas extensiones de apache frente a la robustez de los servidores de aplicaciones web para java).

Por ello jython delega esta gestión de hilos delegando en el JVM e, incluso, delega en él la _[recolección de basura][2]_ (_garbage collection_). Como consecuencia directa, en jython no existe el odioso **[GIL][]** de CPython que impide que dos hilos se ejecuten simultáneamente.

[2]: http://es.wikipedia.org/wiki/Recolecci%C3%B3n_de_basura
[gil]: http://en.wikipedia.org/wiki/Global_Interpreter_Lock

## Base de datos

La conectividad con bases de datos en Jython se realiza mediante los conectores [JDBC][] de java, que es una especie de estándar en java que toda base de datos ofrece. En jython, gracias al grandioso módulo `zxJDBC` podemos usar conexiones `jdbc` del modo habitual en python, o sea, mediante la DB-API2. La ventaja es que sólo necesitamos añadir el conector `jdbc` (un fichero `.jar`) a la ruta de clases del JVM, sin tener que instalar la librería o todo el cliente completo como exigen algunas bases de datos en CPython.

En mi caso concreto, necesito conectarme a varios tipos de bases de datos diferentes para interoperar entre ellos. Me resultaba complejo tener que ir instalando las librerías de conexión para el sistema, con algunos pidiendo que te instales el cliente completo con licencia. Además, tenía que instalar los módulos de python, que no siempre estaban actualizados o, simplemente, no existían. Con jython, tengo todos los conectores `jdbc` en un directorio y con sólo un módulo, `zxJDBC`, tengo todo lo necesario.

¿Y sqlite? Python incluye sqlite como base de datos sencilla. Al estar programada en C no aparece con jython. Como alternativa, podríamos usar la `javadb` (aka `derbydb`) que se suele instalar junto con el java, aunque es algo de lo que no podemos fiarnos. Mi recomendación es usar [h2][]. En un fichero de poco más de 1 Mb tenemos una implementación completa de base de datos relacional (SQL-92), tremendamente rápida en comparación con otras, que tiene acceso a través del sistema de ficheros al estilo sqlite o acceder en compartido como servidor TCP/IP, con interface de línea de comandos, con su administrador web,... Es ideal para hacer de intermediario entre bases de datos, aceptando enlaces JDBC a otras bases de datos e importaciones/exportaciones en formato CSV.

[jdbc]: http://es.wikipedia.org/wiki/JDBC
[h2]: http://h2database.com

## Contendores Java

Otro aspecto interesante son los contendores para aplicaciones java (J2EE). Una aplicación jython puede, del mismo modo que hace java, desplegarse en estos contenedores para aprovechar sus servicios j2ee como sería un pool de conexiones para una base de datos. Impresionante, resulta ver que con la versión 3 de [glassfish][] ya se incluye un contenedor específico para jython, lo que permite desplegar en él aplicaciones desarrolladas en [django][] ó [pylons][] (éste último todavía en fase de pruebas) sin cambiar una sóla línea de código.

[glassfish]: http://glassfish.java.net/
[django]: https://www.djangoproject.com/
[pylons]: http://pylonsproject.org/

---

_(CONTINUARÁ)_

Espero haber conseguido interesarte con este artículo. Mi intención es continuar hablando de jython en próximos artículos y mostrar su uso en desarrollos de todo tipo.
Nos veremos pronto.

[^1]: En próximos artículos veremos cómo usar `virtualenv` para crear estos entornos portables.
