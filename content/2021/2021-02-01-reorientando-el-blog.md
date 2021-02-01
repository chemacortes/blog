---
Title: Reorientando el blog
Date: 2021-02-01 21:00:00
Modified: 2021-02-01 20:54:25
Category: Pensamientos
Tags: functional-programming, python, algebraic-data-type, haskell, elm, ihp, nix, purescript, elixir, phoenix, go, racket, lop, mps, tiddlywiki, metaprogramming
Slug: reorientando-el-blog
Authors: Chema Cortés
Summary: Sobre este blog, lo último que he estado investigando y a hacia dónde pienso que irá la programación.
Lang: es
Translation: false
Status:
---

## Introducción

**Año 2020** Un año en el que parece que han pasado muchas cosas, pero que en
realidad no han pasado tantas cosas. Todo se quedó suspendido en espera de
mejores tiempos.

He aprovechado este año para descubrir algunos lenguajes de programación y
tecnologías que, en mi opinión, han de crecer mucho en los próximos años.
También me ha dado tiempo de reflexionar del modo en que se está programando
actualmente y convencerme de lo imposible que es que se cambien algunas cosas.

**La programación ha sucumbido al _formalismo_**. Grupos de trabajo
interdisciplinares se basan en el tradicional modo imperativo de programar, via
común para compartir conocimientos y proponer nuevas ideas. Las ideas
_funcionales_ no tienen cabida y se ven exóticas, incluso contraproducentes para
espíritu colaborativo. Las optimizaciones se centran en mejorar la ejecución de
un programa y ningún esfuerzo se emplea en su correcta formulación matemática.
Como consecuencia, los errores son imprevisibles y difíciles de corregir, algo
que se asume como normal, sin ningún fundamento matemático que guíe el
desarrollo.

Las reflexiones que pongo a continuación solo buscan crear algo de curiosidad en
el lector. Ya no busco convencer a nadie. Dentro de lo posible, ampliaré estos
temas en próximas entradas en el blog, aunque serán casi más pensamientos
fugaces que artículos completos.

## Principios

Aunque suene a _perogrullo_, cuando se produce un fallo en una aplicación es
casi siempre por una condición que no se tuvo en cuenta. Se tratan de
excepciones que no son interceptadas, alguna entrada inesperada para la que no
se escribió un tratamiento, etc, etc. En entornos multitareas, se suma la poca
previsión que se tiene para compartir recursos entre tareas, faltando capacidad
para ver la historia completa de la interacción de todas las tareas.

Es muy dificil escribir un programa que no falle. Pero sí que se pueden seguir
pautas que ayuden a minimizar el impacto, sobre todo que ayuden a prever desde
el primer momento los posibles fallos. Los compiladores son cada vez más
inteligentes y los entornos de desarrollo ofrecen al instante ayudas para
corregir posibles fallos en el código.

De mi experiencia personal con varios lenguajes de programación, creo que hay
algunas características que debe tener un lenguaje de programación para evitar
errores. No son exactamente características que hagan más fácil la programación,
por lo que costará que un programador las tenga en cuenta. Algunas requierán
tener bastante disciplina; en cambio otras implica tener que cambiar de lenguaje
de programación.

### Tipado de datos

Es muy pesado expresar siempre el tipo de dato de todos y cada uno de los
objetos que usamos en un código. Hay veces que incluso no conocemos qué tipos
van a tener hasta el momento de ejecutar el código.

En general, tenemos dos estrategias:

* Tipado estricto: donde se indica explícitamente el tipo de todos los objetos
* Tipado gradual: donde se indica el tipo de algunos objetos como anotación

Hoy en día, algunos lenguajes con tipado estricto (eg: scala) poseen _inferencia
de tipos_, o lo que es lo mismo, son capaces de determinar el tipo de dato a
partir del contexto, lo que hace más cómodo programar con ellos.

Para lenguajes de tipado gradual (eg: python), también existen herramientas de
desarrollo capaces de inferir el tipo de dato, mostrando opciones para hacerlo
explícito.

La sensación es que ambas estrategias tienden a coincidir, requiriendo
únicamente expresar aquellos tipos que sean más importantes o que pueden influir
significativamente en el resto del programa.

Sin embargo, hay una gran ventaja al contar con un sistema de tipos estrictos:
los [_tipos algebraicos_][1]. Normalmente, los cambios de estado requieren de
una programación meticulosa para no dejar ningún caso sin cubrir, siendo
complicados de mantener sin cometer errores. Con los tipos algebraicos se puede
modelizar la lógica existente en los cambios de estado, asegurando que no queda
ningún caso sin cubrir.

### Programación funcional

He hablado bastante en este blog sobre mi predilección por la _programación
funcional_. Podemos destacar algunas características como el uso para todo de la
recursividad, no tener variables, todo es inmutable sin efectos colaterales,
etc. Pero si hay una cosa que la define sobre todas las demás es la capacidad
para retrasar la evaluación y las excepciones hasta el momento que sea
necesario.

La capacidad de _diferir_, además de ahorrar en cálculos innecesarios, permite
realizar un mejor seguimiento paso a paso de un código, lo que mejora nuestra
capacidad de comprender y razonar sobre su funcionamiento.

### Concurrencia

Hay muchos mitos alrededor de la concurrencia. El más común es pensar que puedes
programar igual si hay un hilo de ejecución como si hay muchos. También está el
que confunde paralelizar la ejecución con paralelizar los datos. Como se suele
decir, no existe _una bala de plata_ que sirva para todos los casos. En
concurrencia, cada problema tiene una solución distinta.

Necesitamos poder _razonar_ sobre el funcionamiento de un código en
concurrencia, algo muy dífícil si no usas programación funcional.

Hay muchos lenguajes que aseguran ser los mejores para programación en
concurrencia. En mi opinión, ninguno es capaz de dar una solución, aunque
algunos se aproximan más que otros. Intentaré dar algunas comparativas en
próximos artículos.

## Lenguajes

### Python

Hoy en día, python se ha hecho popular entre iniciados a la programación y
programadores científicos. Se puede llegar a decir que **_"no has entendido un
código si no lo puedes explicar con python"_**. Es por ello que intentaré
expresar algunos conceptos en python, a pesar de sus limitaciones para algunas
tareas. Servirá de comparación con el modo que usan otros lenguajes para ofrecer
algunas soluciones.

De todos modos, me dicen mucho que mi código python no parece código python. En
realidad, no hago más que aplicar el conocido como _"estilo pythónico"_ y que
ayuda a crear código más simple y mantenible. Lamentablemente, hay muchos
programadores python que desconocen toda la potencia que tiene el lenguaje y
algunos módulos de su librería estándar que simplifican mucho algunas tareas.

### Haskellers

Bajo la denominación de _"haskeller"_ me refiero a varios lenguajes basado en
haskell y su ecosistema.

El lenguaje [Elm][] surge como _framework_ para crear aplicaciones webs cliente
que corran en el navegador (javascript). Su modelo de funcionamiento, llamado
**TEA** por _"The Elm Architecture"_, simplifica la creación de webs dinámicas,
desacoplando la lógica de la visualización, minimizando la posibilidad de
cometer errores.

Elm es uno de los descubrimientos de este año. Es divertido crear aplicaciones
con este lenguaje y realmente ayuda a cometer muchos menos errores. Lo único
malo son [algunas dudas][2] sobre las decisiones que están tomando sus
diseñadores sobre su futuro, algo que no ayuda mucho para su adopción en
sistemas en producción.

Aún así, Elm es un referente que recomiendo y del que se están inspirando muchos
frameworks para otros lenguajes.

Una alternativa directa a elm sería [purescript][], considerado como el _haskell
para javascript_. Tiene varios frameworks web, algunos inspirados en la
arquitectura elm. No obstante, la curva de aprendizaje es algo mayor, sin
conseguir la misma funcionalidad.

Otra sorpresa ha sido el framework [IHP][], un MVC programado en haskell. Posee
un interface administrativo, muy similar al de django, desde el que se puede
gestionar la base de datos, así como generar código haskell para los distintos
elementos. Su gestión de dependencias se hace a través de [nix][], lo que
garantiza la reproducibilidad y los despliegues seguros.

A partir de una serie de artículos sobre la [creación widgets en elm para
IHP][3], se pueden considerar el dúo IHP/elm como el entorno fullstack ideal
para programadores haskell.

### Elixir

Dentro de las opciones funcionales, también he mirado algo de [elixir][] y su
framework [phoenix][]. Tienen fama de soportar grandes cargas de trabajo y
seguir ofreciendo alta disponibilidad, aunque estoy convencido que hay
soluciones similares en otros lenguajes (eg: go). De momento, lo tengo aparcado.

### Otros lenguajes

No me olvido de lenguajes como scala o coconut, de los que he hablado mucho en
este blog. En el caso de scala está a punto de salir la versión 3, cuyo
compilador se conoce como _dotty_ y que será un gran avance para este lenguaje.

Rust también tiene bastante interés. Su _toolchain_ para _webassembly_ (_wasm_)
lo posiciona como el lenguaje para programar componentes web nativos (no
javascript). Sería posible crear _frontend_ en el navegador programados con elm
para manejar el entorno gráfico (árbol DOM) y usar rust/wasm para los módulos
que requieran cálculo intensivo. De rust también es interesante su sistema de
_préstamo_ de variables que evitar errores al compartir variables en
concurrencia y que hace innecesario un recolector de basura.

Otro lenguaje que he retomado es racket. Es un lenguaje funcional tipo lisp o
scheme. Lo que lo diferencia es que se puede usar para crear nuevos lenguajes.
Es lo que se conoce por _"Programación orientada al lenguaje"_ (LOP -
Language-oriented Programming). La idea es crear un lenguaje próximo al usuario
con el que pueda describir los requisitos que ha de tener una aplicación y que
podamos usar como _"contrato"_ de lo que tiene que hacer una aplicación.

Existe algo similar ofrecido por Jetbrain, el [MPS][]. Está mejor documentado y
el entorno IDE es inmejorable. Seguramente empiece por él.

También habrá espacio para la _metaprogramación_. Lo pongo casi al final puesto
que será el tema del próximo artículo, que no tardará mucho.

### Tiddlywiki

Por último, otra de las locuras en las que estoy metido es en la programación de
entornos de desarrollo para [tiddlywiki][]. Lo normal en tiddlywiki es tener un
fichero html que incluye todo el código javascript junto con los contenidos
(_tiddlers_). Pero también se puede tener un entorno node de trabajo que permite
realizar algunas tareas y lanzar algunos scripts.

[1]: https://en.wikipedia.org/wiki/Algebraic_data_type
[2]: https://lukeplant.me.uk/blog/posts/why-im-leaving-elm/
[3]: https://driftercode.com/blog/ihp-with-elm-series/
[elm]: <https://elm-lang.org/>
[purescript]: <https://www.purescript.org/>
[ihp]: <https://ihp.digitallyinduced.com/>
[nix]: <https://nixos.org/>
[elixir]: <https://elixir-lang.org/>
[phoenix]: <https://www.phoenixframework.org/>
[mps]: <https://www.jetbrains.com/mps/>
[tiddlywiki]: <https://tiddlywiki.com/>
