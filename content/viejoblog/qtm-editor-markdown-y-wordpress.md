---
Title: qtm: un editor para markdown y wordpress
Date: 2011-05-22 20:34
Modified: 2022-07-19 21:01:36
Author: Chema Cortés
Category: Técnicas
Tags: markdown
Slug: qtm-editor-markdown-y-wordpress
Status: hidden
---

Buscando una aplicación para hacer más cómodas mis publicaciones en wordpress que, además, aceptara markdown, he estado a apunto de abandonar. Nigún cliente acepta *markdown* y, el único editor de *markdown* que he encontrado, [retext][][^1], no tiene opción para publicar en blogs.

Finalmente me he encontrado con esta joya llamada **[qtm][]** desde la que estoy escribiendo este *post*. Es un cliente basado en Qt que permite editar el artículo *fuera de línea*. Puede usar *markdown* tanto para la previsualización como para la conversión a html antes de enviar a wordpress. En mi caso, como ya tengo activado un plugin en wordpress para markdown, envío el artículo direstamente en markdown sin procesar a html.

Es necesario actualizarse a la última versión de **qtm** ya que con la versión que instala por defecto ubuntu me daba algunos problemas con las categorías y etiquetas. Para instalar la última versión, basta con añadir el repositorio PPA siguiente:

	$ sudo apt-add-repository ppa:indigojo/ppa
	$ sudo apt-get update
	$ sudo install qtm

[retext]: http://sourceforge.net/p/retext/home/
[qtm]: http://qtm.blogistan.co.uk/ "QTM The open-source blogging client"


[^1]: **retext** es una utilidad para *markdown* que debería añadir a las que puse en mi anterior artículo. Puede previsualizar el resultado final a la vez que se va escribiendo. También tiene opciones para convertir un texto *markdown* a otros formatos como odt y pdf.
