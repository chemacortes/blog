---
Title: Renacimiento
Date: 2016-01-10 15:51:06
Author: Chema Cortés
Category: Notas
Tags: python, haskell, scala
Slug: renacimiento
Summary: Pensamientos de lo hecho estos años y qué espero del futuro
---

Si eres uno de los pocos seguidores de este blog, habrás notado que se migrado a un nuevo servidor y un nuevo *framework*.

He tenido el blog bastante abandonado. Podría decirse que no tenía nada interesante qué decir en este tiempo, pero la verdad es que  he preferido contar lo poco que tenía que contar a través de [twitter] y otras vías alternativas.

Si esperas que continúe con los artículos de [Python], es posible que no lo haga. Últimamente, estoy bastante defraudado con los programadores que se acercan a este lenguaje. Puede que sea por haberse convertido en un lenguaje tan popular, algo que siempre es bueno. Pero echo mucho de menos el *"modo pythónico"* que influía en todo lo que se hacía para este lenguaje en sus principios. Ahora parece como que haya que programar para que lo entiendan incluso los que no saben python. Se evitan usar compresiones de listas o expresiones generadoras porque son técnicas demasiado avanzadas, y las novedades que introduce python3 parece como que haya que evitarlas. Me parece *simplemente absurdo*.

Creo que python es un lenguaje genial para *scripting*, con ámbitos de aplicación que abarcan desde gestión de sistemas a aplicaciones científicas. *Un lenguaje para gobernarlos a todos*. Pero necesita evolucionar, y necesita un mejor sistema de tipos. El *tipado gradual* es imprescindible y debería ser aceptado por la comunidad de programadores python cuanto antes (tema que espero tratar en algún próximo artículo).

Sigo usando mucho python. De hecho, este blog está ahora creado con [pelican], un generador estático de páginas html. También me ayudo de varias herramientas python en tareas tales como el *push* al repositorio de github donde alojo ahora el blog (posiblemente, también sea objeto de un nuevo artículo cómo lo hago). Por si fuera poco, también uso [gedit] para editar el texto, donde estoy incorporado algunos *snippets* en python para dar formato al texto *markdown* (vale, tomo nota para otro artículo).

Este último año, creo que el lenguaje en el que más he programado ha sido [haskell]. Aunque ya muchos años, es en estos momentos cuando se está produciendo un autentico *"Renacimento"* de este lenguaje. De modo similar al periodo histórico, están surgiendo alrededor de este lenguaje verdaderos *hombres del renacimiento* que combinan disciplinas tales como Matemáticas, Filosofía y Ciencias [^1]. Una auténtica ágora virtual de pensadores alrededor de la programación abstracta que no debería perderse nadie interesado en estos temas.

La verdad es que la vejez de haskell se nota en algunos problemas de dependencias entre módulos y la carencia de herramientas de desarrollo modernas. Se está trabajando mucho en hacer de haskell una herramienta con suficiente *"calidad industrial"* como para ser alternativa empresarial a cualquier otro lenguaje de programación [^2].

Aún con todo, sigo programando en [scala]. Es el lenguaje con el que me siento más cómodo. Este último año ha estado marcado por la popularización del transpiler [scala.js] para javascript, algo que está atrayendo más desarrolladores a scala que su contraparte para JVM. Tengo intención de realizar algunos desarrollos para Angular o React con scala.js y pronto podré contar algunas cosas más.

También este último año he estado usando bastante [jupyter-scala], un kernel scala para el [jupyter-notebook][jupyter], para la realización de diversos ejercicios de bioinformática. Toda una gozada de usar y, sobre todo, de tener documentados todos los pasos que iba dando. Si os interesa la bioinformática, os recomiendo la serie MOOC sobre [bioinformática][1] de la UCSanDiego, unos cursos prácticos donde se combina la algorítmica con los distintos descubrimientos que se han ido produciendo en biología genética. *Clases magistrales de hacking del bueno*.

Pero si hay algo que me sigue entusiasmando de scala es la gran cantidad de avances técnicos que tiene. El compilador de scala es, en mi opinión, uno de los mejores que existe. Innovaciones como *"macros"*, programación genérica con [shapeless], las [akka-streams] para microservicios o la reciente [rapture.io], con una API magistralmente diseñada, da idea del dinamismo que tiene este lenguaje. Algo que cuesta ver en otros lenguajes.

En fin. Espero poner en claro mucho de lo dicho aquí. También espero que mis nuevas entradas en el blog sean más frecuente. Hasta pronto.

[^1]: Sin menoscabo de otras expresiones artísticas como [The Haskell School of Music](http://haskell.cs.yale.edu/?post_type=publication&p=112).
[^2]: Una de la empresas que más está dinamizando haskell es [FPComplete], introduciendo haskell en los desarrollos para las grandes empresas.

*[JVM]: Java Virtual Machine
*[transpiler]: compilador código fuente a código fuente

[twitter]: https://twitter.com
[python]: http://python.org
[pelican]: http://getpelican.com/
[gedit]: https://wiki.gnome.org/Apps/Gedit/ "Gnome Editor"
[haskell]: https://www.haskell.org/
[fpcomplete]: https://www.fpcomplete.com/
[scala]: http://scala-lang.org/
[transpiler]: https://en.wikipedia.org/wiki/Source-to-source_compiler
[scala.js]: http://www.scala-js.org/
[jupyter-scala]: https://github.com/alexarchambault/jupyter-scala
[jupyter]: http://jupyter.org/
[1]: https://www.coursera.org/specializations/bioinformatics
[shapeless]: http://typelevel.org/
[rapture.io]: http://rapture.io/
[akka-streams]: http://akka.io/
