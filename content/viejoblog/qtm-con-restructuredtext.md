---
Title: qtm con reStructuredText
Date: 2011-05-24 01:49
Author: Chema Cortés
Category: Python
Tags: restructuredtext, tip
Slug: qtm-con-restructuredtext
---

Puestos a explotar todas las posibilidades de la utilidad [qtm][], también es posible emplear esta utilidad para previsualizar y subir al blog artículos escritos en **[reStructuredText][2]** (abreviadamente ReST) en lugar de *markdown* que viene por defecto.

De la instalación de **[docutils][1]** obtendremos las herramientas básicas con la que crear documentación para python. Una de estas herramientas es `rst2html`, con la que podríamos convertir un artículo en ReST a html antes de subirlo. El problema es que esta conversión se realiza como documento completo, con las secciones `<head>` y `<body>` típicas de un documento html, lo que no va bien si queremos insertar la salida de este comando a la entrada de nuestro blog.

Como solución, podríamos crear una plantilla para `rst2html` que sólo contenga la parte del `<body>`, pero hay una alternativa mejor: usar el script [rst2wp][] de *Matthias Friedrich*. Colocamos este script en un directorio apropiado (eg: `/home/usuario/bin`) y configuramos *qtm* de la siguiente manera:

![qtm para ReST]({static}/pictures/qtm-para-ReST.png)

Como ya comenté en anteriores artículos, para escribir en páginas web resulta más sencillo usar `markdown` o `markdown extra`, pero a veces no queda más remedio que emplear ReST cuando necesitamos escribir documentación técnica en determinados blogs. Con *qtm* tenemos una herramienta sencilla para estos cometidos.


[qtm]: http://qtm.blogistan.co.uk/ "QTM The open-source blogging client"
[1]: http://docutils.sourceforge.net "docutils"
[2]: http://docutils.sourceforge.net/rst.html "reStructuredText"
[rst2wp]: http://unmaintainable.wordpress.com/2008/03/22/using-rst-with-wordpress/

*[ReST]: reStructuredText
