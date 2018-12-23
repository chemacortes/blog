Title: Lenguajes de marcas ligeras
Date: 2011-05-17 02:13
Author: Chema Cortés
Category: Técnicas
Tags: calibre, markdown, pandoc, restructuredtext
Slug: lenguajes-de-marcas-ligeras

# ¿Para qué usar Lenguajes de Marcas Ligeras?

Últimamente he estado estudiando el uso [markdown][1] en diferentes niveles. Por el tipo de actividad que realizo, tengo que generar mucha documentación para acompañar código de programación y no resulta práctico tener que generar a mano los diversos formatos de documentos que se puedan necesitar. Es fundamental poder escribir un sólo documento y generar a partir de él todos los demás formatos.

Los [*Lenguajes de Marcas Ligeros*][2] como markdown permiten tener un documento en texto plano suficientemente *"legible"* para su uso como documentación interna en un proyecto y convertir después a otros formatos para presentaciones, publicación web o, simplemente, para su archivo. Estos lenguajes de marcas hacen muy cómodo el incorporar pequeños fragmentos de código durante el proceso de redacción, que aparecerán en el documento final con sintaxis coloreada gracias a varios *plugins*. Además, al ser documentos en texto plano, encajan perfectamente con el sistema de control de versiones de código que se use en el desarrollo.

[1]: http://daringfireball.net/projects/markdown
[2]: http://es.wikipedia.org/wiki/Lenguaje_de_marcas_ligero
[3]: http://mitcho.com/code/

# markdown, markdown extra y reStructuredText

[**Markdown**][1] se centra en la generación de documentos HTML, algo bastante apropiado para su uso en blogs y wiki [^1]. La principal virtud de markdown es su *"legibilidad"* a pesar de tener contenida toda la información necesaria para generar la estructura del documento HTML, aunque resultará demasiado simple para crear documentación avanzada con tablas, notas bibliográficas, tablas de contenidos,...

Son muchas las propuestas para añadir a markdown nuevos elementos. Estas extensiones del lenguaje hacen que tengamos que indagar si una herramienta nos es útil o no según si acepta la extensión que estemos utilizando. De entre todas las extensiones, la más aceptada es la ["PHP Markdown Extra"][4], o simplemente **"markdown extra"**. Casi se puede asegurar que toda herramienta que procese *markdown* acepta también *markdown extra* ([markdown para wordpress][3], [python-markdown][], [pandoc][], ...).

Pero si nuestro objetivo es crear documentación más "profesional", *markdown* se nos quedará corto enseguida. Antiguamente, toda la documentación se realizaba en [$\LaTeX$](http://www.latex-project.org/ "LaTeX"), a partir del cual se podía generar documentos de cualquier formato y siempre con una calidad tipográfica profesional. Hoy en día, $\LaTeX$ sigue siendo usado en la generación de los documentos finales, pero en la redacción de la documentación se están usando herramientas que simplifiquen la labor y, sobre todo, que consiga mejor legibilidad que un documento en formato $\LaTeX$.


Como alternativa a $\LaTeX$, sin duda destaca el languaje de marcas [**reStructuredText**][rst]. Ligero, muy completo y legible. Posee cualquier elemento que necesite nuestro documento, con conversores de formato a casi cualquier cosa (incluido $\LaTeX$). La documentación de python es un buen ejemplo de lo que se puede hacer con reStructuredText junto con [sphinx][] (Tema que abordaré en un próximo artículo).

[4]: http://michelf.com/projects/php-markdown/extra/ "PHP Markdown Extra"
[python-markdown]: http://www.freewisdom.org/projects/python-markdown/
[pandoc]: http://johnmacfarlane.net/pandoc/
[rst]: http://docutils.sourceforge.net/rst.html "reStructuredText"
[sphinx]: http://sphinx.pocoo.org/

# Herramientas markdown

De momento, dejo *reStructuredText* para otro momento y me voy a centrar en *markdown* (y *markdown extra*). Como he dicho, el destino final de *markdown* es generar ficheros HTML; pero existen dos maneras sencillas de generar otros formatos:

-   **[Pandoc][]**: es una herramienta que se puede usar para convertir entre *markdown* y *reStructuredText*, así como para generar otros muchos formatos como `html, s5, docbook, opendocument, latex, context, texinfo, man, mediawiki` y `rtf`. La calidad de los documentos generados dejan mucho qué desear, pero como conversor entre *markdown* y *reStructuredText* hace un buen papel.

-   **[calibre][]**: se trata de uno de los más conocidos gestores de ebooks, una de las aplicaciones en [python][] más destacadas. Lo que muchos desconocen es que entre los distintos formatos de libros electrónicos que es capaz de convertir admite *markdown* como formato de los ficheros de texto. Es la forma más rápida y sencilla de generar *ebooks* que tenemos a nuestro alcance. Basta configurar que use para la detección de capítulos la expresión `//h:h1` para que nos cree automáticamente una *tabla de contenidos*.

    ![Selección de capítulos](/pictures/Pantallazo.png)

[calibre]: http://calibre-ebook.com
[python]: http://python.org

*[HTML]: Hyper Text Markup Language
*[APIs]: Application Programming Interface (Interfaz de Programación de Aplicaciones)

NOTAS:

[^1]:  Sin ir más lejos, toda esta entrada del blog está escrita en markdown gracias al plugin [markdown][3] para *WordPress*. Esta nota al pie es una característica extra aportada por *markdown extra*.
