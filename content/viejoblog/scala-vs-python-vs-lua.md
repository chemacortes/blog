Title: Scala vs. Python vs. Lua
Date: 2013-04-09 20:55
Author: Chema Cortés
Category: Pensamientos
Tags: python, scala, lua, programming-languages
Slug: scala-vs-python-vs-lua

Hace bastante tiempo que ando comentando cosas de estos tres lenguajes: Scala, Python y Lua. Hasta el momento no he hecho una comparativa entre ellos y creo que es el momento de hacerlo, siempre desde el punto de vista de un programador. Más que llegar a la conclusión de cuál es mejor o peor, quisiera dar una idea de porqué los recomiendo, a los tres, sin decantarme por sólo uno de ellos. Si buscabas razones para quedarte con uno de ellos, tampoco deberías desestimar otros similares como Ruby, Groovy, Haskel, Clojure o Erlang. De todos hay cosas qué aprender.

##Python

Quizás Python sea el lenguaje más asequible para un programador que empieza o que busca un segundo lenguaje. Su aprendizaje es sencillo, mientras que su potencia y ubicuidad lo hace ideal desde los pequeños scripts que podamos necesitar en nuestro día a día, hasta escalar a servidores empresariales de tipo medio.

Puede que a muchos disguste python por su identación forzada o por su particular modelo de datos, por citar dos de las características más criticadas. Sin embargo, confía en mí si te digo que python es uno de los mayores compendios de sabiduría que puedes tener al alcance de tus manos. Cualquier cosa que creas extraña o fuera de lugar, seguramente tenga su buena explicación. El sistema colaborativo que hace evolucionar a python (conocido como PEP-*Python Enhancement Proposals*) consigue que todo el saber de la comunidad python termine decantándose hace un modelo de evolución del lenguaje que lo hace único, con el que mejora calmadamente con cada versión. Operaciones con números grandes, algoritmo MRO para herencia múltiple, estructuras de datos optimizadas (heapq, deque,...), ordenaciones por clave, operaciones sobre secuencias (sum, any, all,...)... son sólo algunos ejemplos de optimizaciones que el usuario usa sin ser realmente consciente de la cantidad de trabajo que le está ahorrando. En python casi siempre hay una forma de hacer las cosas correctamente, y además suele ser la mejor.

##Lua

Desde mi punto de vista, considero Lua como un *python minimalista*. Sin objetos, sin posibilidad de construir tus propios tipos de datos, pero se apaña con un sólo tipo de estrutura `table` para montar un sistema de herencia y emular algunos tipos de datos. Si lenguajes como python te parece complicados, no comprendes conceptos como la herencia, la creación de tipos o para qué sirven las metaclases, la simplicidad de lua hará que entiendas mejor estos conceptos.

El reducido tamaño del intérprete de Lua lo hace apropiado para ser empotrado en otras aplicaciones. Lo tenemos en gestores de paquetes (RPM), bases de datos (mysql-lua), e IDEs (Scite), aunque quizás sea más famoso por ser el motor de script de juegos como *World of Warcraft*.

En cuanto a sintáxis, también goza de un minimalismo que, a veces, desearías tuviera python. Posee cierta relajación en la llamada a funciones que permite usarlo para crear DSLs (*Lenguajes Específicos del Dominio*), aunque quizás su mejor uso sea como lenguaje de descripción de datos en sustitución de xml, yaml o ficheros ini.

##Scala

Reconozco que soy un ferviente partidario de la *Programación Funcional*. Python tiene algún aspecto de este paradigma, pero cada vez parece más diluido dentro del sistema de Clases Abstractas (`ABC`-Abstract Base Classes) que empiezan a generalizarse en python. La estrategia de python es optimizar el uso de estas clases abstractas, independientemente de las clases que deriven luego de ellas. Aunque es un buen enfoque de optimización, siempre estará limitado a tiempo de ejecución.

Scala posee un potente sistema de tipado estático de datos que posibilita la inferencia del tipo de una operación, lo que permite cierta relajación en el tipado que lo hace muy similar al tipado dinámico. Pero la posibilidad de crear nuevos tipos, ya no sólo de objetos, si no también a partir de funciones o de *patrones de código*, consigue interfaces más robustos y que sea el compilador quien optimize el código, antes de su ejecución.

Así que tenemos que scala es funcional, con un potente sistema de tipos y, además, 100% compatible con Java. ¿Se puede pedir algo más?

Pues sí. Incorpora el llamado modelo *Actor* para programación concurrente. Con los actores, en lugar de compartir un espacio común de memoria entre los distintos procesos concurrentes, se establece un sistema de mensajes que son enviados y recibidos. Este modelo se ha mostrado bastante eficaz en sistemas de alta demanda como son algunas webs como twitter o linkedin.

En cuanto a la sintáxis, scala también posee algunas normas relajadas para la creación de DSLs muy similar a lo que se ve en Groovy. Algunos lenguajes DSL se usan en *frameworks* de creación webs, como Play2, o para crear conjuntos de pruebas (ScalaUnit).

##Conclusión

Espero que te haya convencido para que eches un vistazo a algunos de estos lenguajes, aunque los tres sean altamente recomendables. Si tuviera que resumir en pocas líneas lo dicho hasta ahora, sería así:

- Python: navaja suiza de los lenguajes. Sirve para todo y está presente en cualquier sitio. Es un compendio de sabiduría para hacer las cosas de la mejor forma, aún sin proponértelo.

- Lua: lenguaje minimalista. Ayuda a comprender mejor algunos conceptos de programación. Es el lenguaje que me gustaría que tuviera todo navegador en lugar de javascript.

- Scala: funcional y con potente sistema de tipos. Su implementación del modelo actor lo hace idóneo para la creación de sistemas de alta demanda de accesos.
