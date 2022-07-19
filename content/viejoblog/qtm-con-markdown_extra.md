---
Title: qtm con markdown_extra
Date: 2011-05-23 00:00
Modified: 2022-07-19 21:01:00
Author: Chema Cortés
Category: Técnicas
Tags: markdown, tip
Slug: qtm-con-markdown_extra
Status: hidden
---

Por defecto, **[qtm][]** usa el comando `markdown` que se instala en linux en la ruta `/usr/bin/markdown`. Este comando acepta la sintáxis básica de *markdown*, insuficiente cuando estamos acostumbrados a usar la extensión *markdown extra*.

Con un pequeño truco, es posible usar *markdown_extra* con *qtm*. Instalando el módulo [markdown para python][python-markdown] (paquete `python-markdown` en *ubuntu*) obtenemos un comando alternativo llamado `markdown_py` que acepta numerosas extensiones para *markdown*, entre las que se incluye `markdown_extra`.

Para usar *markdown_py* en *qtm*, creamos el pequeño script que active la extensión `extra` en el parseo:

```bash
#!/bin/bash

exec markdown_py -x extra "$@"
```

Llamamos a este script `markdown_extra`, le asignamos permisos de ejecución y lo metemos en algún lugar apropiado como la carpeta `bin` de nuestro usuario linux. En la configuración de *qtm*, introducimos como ruta al comando markdown

	/home/usuario/bin/markdown_extra

A partir de aquí podremos previsualizar nuestro código con `markdown extra`. También podríamos añadir otras extensiones como, por ejemplo, `toc` con la que podemos crear tablas de contenidos:

```bash
#!/bin/bash

exec markdown_py -x extra -x toc "$@"
```

Debemos asegurarnos que nuestro blog posea también esta extensión. Si no la tuviera, siempre tenemos la posibilidad de indicarle a *qtm* que convierta nuestra entrada a html antes de enviarla al blog.

---
**Actualización**

Para windows es necesario otro tipo de configuración. Una vez instalado el módulo `python-markdown` se debe crear un fichero *.bat* en `C:\Python2.7\Scripts` con el siguiente contenido:

```winbatch
@"c:\python27\python.exe" "%1" -x extra -x toc "%2"
```

Si llamamos a este fichero `markdown_extra.bat`, la configuración de *qtm* quedaría de esta manera:

![Preferencias de QTM](/blog/wp-content/uploads/2011/05/Preferencias-qtm.png)

[qtm]: http://qtm.blogistan.co.uk/ "QTM The open-source blogging client"
[python-markdown]: http://www.freewisdom.org/projects/python-markdown/
