---
Title: Scripting para scala
Date: 2021-10-17 12:52:28
Modified: 2021-10-17 12:58:13
Category: Pensamientos
Tags: python, scala, scripting
Slug: scripting-para-scala
Authors: Chema Cortés
Summary: Unos pensamientos sobre mi actual decepción con python y porqué empiezo a usar más scala para tareas de _scripting_.
Lang: es
Translation: false
Status:
---

## Mi decepción con python

Llevo mucho tiempo usando python como lenguaje de _scripting_. Python se ha convertido para mí en un lenguaje imprescindible gracias a su completa librería estándar, así como a la infinidad de módulos para hacer cualquier cosa.

Voy siguiendo su evolución, las nuevas incorporaciones en su sintáxis, así como la evolución de sus herramientas emblemáticas como _jupyter_ o _pandas_, y herramientas de desarrollo como _pyenv_ o _poetry_. No es extraño que se haya convertido en el lenguaje de programación más popular en estos momentos, algo que nadie me creía hace algunos años cuando decía que iba a desbancar a Perl, Ruby y PHP, e incluso a Java o C/C++.

A pesar de esta popularidad de python, y de que cuento en mi arsenal con bastante código que uso a diario, me canso de ver lo mal que se está programando en general con python. De acuerdo que no es un _lenguaje funcional_, como me gustaría que fuera, pero es no se están usando muchas características del lenguaje que harían un código python más expresivo y mantenible.

En particular, me pasa siempre que veo que alguien usa el método `.append()` en las listas. Casi con toda probabilidad, está intentando crear una lista añadiendo los elementos uno a uno, tal como ha aprendido en otros lenguajes de estilo imperativo, en vez de usar las _compresiones de listas_, más eficientes y más simples de trabajar. Lo malo es que cuando hago ver que se puede mejorar ese código me responden que es mejor no usar características propias de python que nadie conoce.

Puede ser discutible si hay que dejar de usar características de python sólo para hacerlo más accesible al público general. Lo que no entiendo es que se esté usando esa excusa para no dedicar esfuerzo en sacar todo el potencial que ofrece python, ni para aprender otros lenguajes de programación que enseñen maneras distintas de programar a lo básico aprendido en clase. Se está enseñando un único modo de programar (imperativo), haciendo creer que tiene que ser el mejor modo, y no lo es.

Mi impresión, ahora mismo, es que da igual si sale una nueva versión de python, si se incorpora sintáxis para programación asíncrona o si se se mejora el tipado gradual con _clases abstractas_. Una gran mayoría seguirá programando python del mismo modo que aprendieron hace años, sin ver necesidad de cambiar nada en su estilo de programar.

## _Tooling_ para scala

Scala es uno de mis lenguajes favoritos. Hace muy poco ha salido la versión 3 (aka _dotty_), más fácil de usar y más potente en algunos aspectos. Ha roto con las limitaciones que le imponía la máquina java para convertirse en un _metalenguaje_ (Algún día tengo que hablar de [TASTy][] y la _metaprogramación_ en scala). Se han aunado esfuerzos en dotar a scala de herramientas de desarrollo excelentes, así como en poder aplicarlo al desarrollo java, graalvm, web (javascript), android o llvm (_native scala_).

Por el lado práctico, la nueva sintáxis de scala3 se aproxima mucho a python. Herramientas como _jupyter_ puede incluir kernels de scala. La comunidad Scala ha creado librerías que emulan en funcionamiento a las conocidas `requests`, `pathlib` o `pandas` de python, por nombrar unas pocas. Si no es suficiente, [scalapy][] permite integrar python en scala, abriendo a scala todo el arsenal de python.

Sin duda, scala se ha convertido en un lenguaje a tener en cuenta. No sólo como un lenguaje _"java mejorado"_, como muchos lo han calificado. Cuenta con potentes herramientas para _scripting_ y desarrollo en general que vale la pena conocer. Pero no sólo eso, también se situa en la vanguardia de una nueva generación de compiladores que añade innovaciones como no se han visto en ningún otro lenguaje.

Mi intención es ir mostrando en este blog algunas herramientas de scala a medida que yo mismo las estudio. De momento, las pruebas que he hecho hasta ahora han sido exitosas, siendo muy cómodo usar scala para scripting, tanto como era python. Mi objetivo final es sustituir, poco a poco, los scripts de python por scala, o intentar combinarlos, ya veré.

<!-- markdownlint-disable MD036 -->
_"And Now for Something Completely Different..._

[TASTy]: https://docs.scala-lang.org/scala3/guides/tasty-overview.html "Typed Abstract Syntax Trees"
[scalapy]: https://scalapy.dev/
