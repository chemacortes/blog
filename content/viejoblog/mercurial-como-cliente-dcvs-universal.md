---
Title: Mercurial como cliente DCVS universal
Date: 2011-08-30 13:14
Modified: 2022-07-19 21:12:19
Author: Chema Cortés
Category: Python
Tags: bitbucket, git, github, mercurial
Slug: mercurial-como-cliente-dcvs-universal
Status: hidden
---

##Introducción

Con la llegada de los [DCVS][] (*Distributed Concurrent Versions System*), se ha convertido en habitual el uso de un sistema de control de versiones en todo desarrollo. La popularización de sitios webs basados en estos sistemas como [github][], [gitorious][], [bitbucket][] o [googlecode][] como foros públicos donde compartir código entre programadores hasta el punto de convertirse en auténticas *redes sociales*, ha hecho de estos sistemas una necesidad para todo desarrollador que se precio, con el consabido dilema de cuál de los sistemas elegir.

Gracias a las extensiones que podemos añadir, cada día es menos transcendente la elección de un DCVS, pudiendo usar cualquier cliente con cualquier otro servidor.

##Comparando git y mercurial

Sin entrar en mucho detalle, podemos comparar estos dos sistemas DCVS populares para hacernos una idea:

###git
* Desarrollado en perl y pensado para linux (mal soporte en windows)
* Velocidad: muy rápido
* Comandos: algo complejo
* Interface gráfico: no tiene
* Popularidad muy alta
* Repositorio público *estrella*: [github][]

###mercurial (hg)
* Desarrollado en python, con versiones para linux, windows y mac
* Velocidad: rápido
* Comandos: sencillo (similar a subversion)
* Interface gráfico: [tortoiseHG][] para gnome y windows
* Popularidad alta
* Repositorio público *estrella*: [bitbucket][]

Éstos son algunos apuntes rápidos. Evidentemente, hay algunos interfaces gráficos para git y es posible emplear git en windows, pero en mi opinión tiene algunos problemas que necesitan pulirse. Por otro lado, existen varios IDEs como netbeans o eclipse que pueden usar cualquiera de estos DCVS, abstrayendo su uso interno a través de un interface común.

Para un programador de **python**, la elección debería ser clara: **mercurial**. Realizado en python y con numerosas extensiones, también desarrolladas en python, parece sin duda la mejor elección. Además, es el sistema de control de versiones más utilizado en proyectos python, incluyendo el desarrollo del lenguaje en si, por lo que se uso es casi obligado si queremos colaborar con otros desarrolladores python.

Pero no hace falta renunciar a nada: desde mercurial también se puede usar repositorios git o subversion. Basta con añadir la extensión adecuada.

En el resto del articulo, me centreré sólo en la extensión [hg-git][], con la que se posibilita el uso de repositorios git desde mercurial, sin necesidad de instalar ningún cliente de git adicional (no existen dependecias con ningún ejecutable `git`).

##hg-git

###Instalación

La última versión de mercurial a la hora de escribir este artículo es la 1.9. Como la versión *"estable*" de hg-git tiene problemas con esta versión en concreto de mercurial, voy a explicar aquí lo que sería el método *manual* de instalación, bastante más seguro.

Suponemos que tenemos ya instalado `mercurial` por lo medios habituales (autoinstalador en windows/instalador de paquetes en linux). Nos será de gran ayuda tener instalado [tortoiseHG][] como interface gráfico para manejar los repositorios. Para windows, la instalación de [tortoiseHG][] incluye todo lo necesario al empotrar un intérprete de python, mercurial y varias extensiones, algunas de ellas necesarias para transformar rutas y nombres de ficheros codificados en MBCS. Los siguientes pasos a ejecutar con mercurial serán más fáciles de aplicar desde la interface de tortoiseHG.

En el emplazamiento que queramos, empezamos por clonar un repositorio con **hg-git** desde mercurial:

```bash
$ hg clone http://bitbucket.org/durin42/hg-git hg-git
```

Normalmente, yo suelo usar un mismo directorio para agrupas todos los repositorios clonados. Ése podría ser el lugar adecuado para guardar este repositorio.

Añadimos esta extensión a la configuración de mercurial. Normalmente, se hace en el fichero `mercurial.ini` (windows) o en `~/.hgrc` (linux). Si usamos tortoiseHG, desde las `"opciones globales"` podemos editar directamente este fichero.

Para añadir la extensión:

```
[extensions]
hggit = <ruta-al-repositorio>\hg-git\hggit
```

Como anotación, en alguna documentación se recomienda añadir también la extensión *opcional* `bookmarks` a la configuración; pero a partir de la versión 1.8 de mercurial, el comando `bookmark` es parte propia de los comandos de mercurial, por lo tanto este paso ya no es necesario.

Como dependencia, hace falta instalar el módulo de python `dulwich` para manejo de repositorios git con python. En windows ya viene incluído en tortoiseHG, por lo que no hay que hacer nada más. En linux, viene como paquete instalable (`python-dulwich` en ubuntu), pero también se podría haber instalado mediante `easy_install` sin mayor problema. Lo que sí hay que tener cuidado es en asegurarnos que no tenemos instalado el paquete `python-git` para que no interfiera con el módulo `hg-git` que estamos configurando.

Como lista final, estas serían las versiones probadas:

* mercurial (hg) `1.9`
* hg-git `0.2.4`
* dulwich `0.6.1`

##Utilización

Con hg-git instalado ya podemos acceder, por ejemplo, a los repositorios de github directamente desde mercurial. Basta con especificar que se trata de un repositorio git:

```bash
$ hg clone git://github.com/django/django.git django.git
```

Para realizar un `push` a github con conexión codificada con SSH:

```bash
$ hg push git+ssh://user@github.com/user/myrep.git
```

Así mismo, si partimos de un repositorio mercurial también podemos *"convertirlo"* para su uso en git con el siguiente proceso:

```bash
$ cd myrep # (dentro del repositorio mercurial)
$ hg bookmark -r default master # marcamos 'default' como 'master'
$ hg push git+ssh://user@github.com/user/myrep.git
$ hg push
```

Al marcar con el nombre `master` a `default` facilitamos la conversión de los datos de mercurial a objetos git. Este proceso sólo es necesario hacerlo la primera vez.

##github o bitbucket

En cuanto a elegir entre github o bitbucket, es más una cuestión de gustos. **github** se ha posicionado como el sistema predilecto para darse a conocer, sobre todo como referencia en los *curriculo* a la hora de solicitar empleo. En cambio, **bitbucket** permite el uso de repositorios privados, muy útil para pequeños grupos de trabajo y para colaboraciones en la *"nube"* (dispositivos móviles).

Ambos son gratuitos, por lo que no debes dejar de probarlos tan sólo por lo que haya podido decir aquí. Es una nueva forma de conocer y darse a conocer entre programadores, algo que sin duda hace de nuestro pequeño mundo algo mucho más grande.

[DCVS]: http://en.wikipedia.org/wiki/Distributed_Concurrent_Versions_System "Distributed Concurrent Versions System"
[github]: http://github.com
[gitorious]: http://gitorious.org/
[bitbucket]: http://bitbucket.org
[googlecode]: http://code.google.com/
[tortoisehg]: http://tortoisehg.bitbucket.org/
[hg-git]: http://hg-git.github.com/
