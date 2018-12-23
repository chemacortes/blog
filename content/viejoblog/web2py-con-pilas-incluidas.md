Title: web2py, con pilas incluidas
Date: 2011-12-01 19:34
Author: Chema Cortés
Category: Python
Tags: jquery, web2py, webdev
Slug: web2py-con-pilas-incluidas

He estado últimamente trabajando en varios proyectos que me han hecho descuidar un poco el blog. En próximos días espero publicar algunos artículos relacionados que creo serán de interés.

Lo último que estoy haciendo es un desarrollo de aplicación de escritorio con [web2py][], a pesar de tratarse de un framework para crear aplicaciones web. Corre desde un navegador cualquiera, interaccionando con [jQuery] para la presentación, y con python corriendo por debajo para dar soporte a la capas de datos y lógica de negocio.

##¿Por qué web2py?

Como indico en el título, web2py lleva las _"pilas incluidas"_, que tratándose de python significa que incluye todo lo puedas necesitar. ¡Y no exagero! La selección de [librerías][3] que incluye es extensa, permitiendo desarrollar casi cualquier aplicación web que necesites, con herramientas administrativas tanto para el modelo de datos como para editar los ficheros vistas y controladores. Vamos, que con descomprimir el fichero con web2py y un navegador ya tienes todo lo necesario para desarrollar la aplicación, desde una simple aplicación estática, hasta una completa aplicación que funcione en el Google AppEngine. Además posee un sistema de plugins que permite cambiar fácilmente el diseño de la web o añadir funcionalidades.

Hasta ahora, había probado algunos GUIs graficos como pyqt o wxpython que incluyeran algún _widget_ html para renderizar páginas webs y poder controlarlas desde el programa python, algo bastante costoso de programar y con serias incompatibilidades a la hora de presentar la página web. Con web2py, la aplicación de escritorio se orienta a una aplicación web con el servidor web corriendo directamente en el cliente. Web2py permite abstraer algunas facilidades ajax y jquery habituales, aunque no resulta difícil usar el resto de funcionalidades de jquery en las aplicaciones sin tener que ser un experto en programación javascript.

Uno de los problemas que también había tenido hasta ahora era en la distribución de aplicaciones python para windows. Habitualmente, hace falta instalar varias herramientas en el sistema, desde el intérprete python hasta todas las librerías necesarias, algunas complicadas de hacerlas funcionar. Bien es cierto que existen formas de empaquetar una aplicación usando py2exe (py2app en MacOS), pero casi siempre hay alguna cosa que no funciona bien del todo. Web2py viene con todo empaquetado para su uso en windows y macOS, incluyendo el intérprete python y resto de librerías necesarias. Basta descomprimir el fichero y, sin intalación, ejecutar el servidor web y abrir un navegador. Las aplicaciones web son carpetas que podemos copiar de una instalación a otra o, aún más sencillo, usar el interface administrativo para empaquetar e instalar aplicaciones (al estilo _tomcat_).

Échale un vistazo, y no te dejes las ["pilas"][3].


[web2py]: http://www.web2py.com
[jquery]: http://jquery.com
[3]: http://www.web2py.com/book/default/chapter/04#Libraries
