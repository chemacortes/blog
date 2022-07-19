---
Title: Programación. ¿Ciencia o Ingeniería?
Date: 2012-03-09 22:21
Modified: 2022-07-19 20:59:47
Author: Chema Cortés
Category: Pensamientos
Tags: science, engineering, programming
Slug: programacion-ciencia-o-ingenieria-2
Status: hidden
---

Cuando inicié este blog, además de servir de soporte a algunos artículos técnicos sobre programación que fueran más o menos novedosos, también me movió la idea de aportar reflexiones sobre algunos temas *interdisciplinares* que constantemente me hacía debido a mi formación científica y que he ido acumulando durante todos estos últimos años. Creo que es momento de empezar con ellos...

## En busca de la materia gris

Todavía persiste el mito de considerar que un informático es una especie de chamán que con unos cuantos pases mágicos delante de una pantalla es capaz de hacer que un ordenador tome vida. Muy pocos asumen que un informático pueda tener una formación científica o técnica seria que se encuentre al mismo nivel que un médico o un ingeniero. Y así nos van las cosas.

No tomarse en serio la formación de un informático está llevando a que muchas empresas del sector no valoren suficientemente la destreza de sus empleados. Asumen que siempre podrán encontrar nuevos empleados a los que poder darles una pequeña formación suficiente para encargarse de cualquier proyecto que tengan en marcha. Si supieran un mínimo de ingeniería, sabrían que siempre hay un límite en todo proyecto en el que añadiendo más recursos nunca se consigue acelerar el desarrollo, si no más bien lo contrario. Momentos de dificultad que desemboca en una crisis[^1], donde prima más la experiencia que la cantidad de manos disponibles.

La actual crisis económica ha venido a agravar más el panorama al minusvalorar aún más a los profesionales de informática. Los buenos profesionales optan por emigrar a otros países donde sean mejor considerados, mientras que aquí las empresas compiten bajando más y más los precios, sin tener en consideración ni la calidad ni la idoneidad del producto que desarrollan.

Estamos inmersos entre sistemas informáticos y de telecomunicaciones que se están colapsando debido a malos diseños y falta de mantenimiento, con usuarios que asumen por normal que un sistema pueda fallar, que los virus puedan entrar hasta las entrañas del ordenador, o que un *hacker* pueda bloquear cualquier sistema gubernamental y robar identidades,... y lo único que importa a los responsables es que alguna empresa sin escrúpulos asuma la culpa por el menor precio posible.

## El fin de la ley de Moore

Es sabido que por la [Ley de Moore][moore] en estos 50 años pasados, se estaba cumpliendo que cada dos años los ordenadores doblaban su velocidad, mientras se hacían cada vez más y más baratos. Como consecuencia, las aplicaciones mal diseñadas aún se podían sobrellevar gracias a la reducción de costes y mejoras de velocidad que ofrecían los nuevos sistemas.

Lamentablemente, la ley de Moore llega a su final. Se intenta prorrogar su vigencia metiendo más *cores* en cada cpu, pero si bien se sigue contando con procesadores más baratos y más rápidos, un sistema multicore no es aprovechable por una aplicación mal diseñada. Para aprovechar una cpu multicore, se requiere de nuevas aplicaciones diseñadas específicamente para ellos. Hoy en día, muchos sistemas operativos sólo son capaces de aprovechar un core de todos los disponibles, lo que no deja de ser un engaño para el usuario que piensa que debería ir todo más rápido. Estamos muy cerca de una nueva crisis similar a la crisis del software, pero con hardware esta vez.

Es una burbuja que pronto va a estallar como tantas otras antes.

## Poner en valor al programador

Hace tiempo que se perdió el significado de ser un **"programador"**. Con ese nombre se ha pasado a denominar un puesto técnico de trabajo que está por debajo de analista y un poco por encima de reparador de hardware. Nada que tenga qué ver con un trabajo metodológico y, en cierta medida, creativo.

Y, sin embargo, contar con buenos programadores debería ser parte del activo de una empresa que la ponga en valor. No es entendible que haya empresas que busquen programadores después de haberse comprometido con un proyecto de desarrollo. Debería ser más bien al revés, que para conseguir un proyecto se haya valorado antes qué programadores dispone la empresa en nómina.

Puedo asegurar que hay alguna empresa que cuenta con un núcleo de buenos programadores, normalmente gente joven que montan su propia empresa, que nunca les falta trabajo. Pero son mucho más numerosas las empresas vacías que se dedican a quemar sistemáticamente a toda su plantilla en proyectos difíciles de asumir sin la gente y los medios adecuados.

Contar con programadores experimentados no es tarea fácil. Toda empresa debería asegurar a sus programadores más valiosos, nunca deberían considerarlos inferiores a analistas, ya que asumen roles distintos. Un buen programador puede ser un pésimo analista y viceversa. Un buen programador debería estar bien pagado simplemente como programador, y no verse presionado para ser analista si quiere ascender y cobrar más.

## Programación. ¿Ciencia o Ingeniería?

Según donde busques, la programación es parte de la *Ciencia de la Computación* o es parte de la *Ingeniería del Software*. Personalmente, me inclino más por que sea una ciencia.  Un buen programador siempre intenta comprender el funcionamiento de un programa con el fin de crear nuevos y mejores programas. Usa un ciclo de análisis, desarrollo, prueba y refactorización que tanto se parece al *"método científico"*, experimentando hipótesis hasta dar con una solución. La ingeniería entraría cuando se requiere que la aplicación se ajuste a determinados requisitos, donde a veces no importa tanto la optimización del programa como el que se ajuste su funcionamiento a los parámetros requeridos.

¿Es posible buscar la belleza entre líneas de código? ¿Evolucionamos hacia mejores lenguajes de programación?

Temas para próximos artículos.

[^1]: véase [Crisis del Software](http://es.wikipedia.org/wiki/Crisis_del_software)

[moore]: http://es.wikipedia.org/wiki/Ley_de_moore "Ley de Moore"
