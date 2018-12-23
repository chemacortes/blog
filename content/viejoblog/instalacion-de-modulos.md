Title: Instalación de módulos
Date: 2012-07-24 22:02
Author: Chema Cortés
Category: Python
Slug: instalacion-de-modulos

Resulta habitual la instalación de nuevos módulos o paquetes en nuestra instalación de python, para lo que basta con introducir en el directorio `site-packages` el fichero del módulo o, en caso de paquetes, el directorio con el paquete. Algunas veces, la instalación requiere compilar e instalar librerías en el sistema, por lo que la instalación se complica bastante.

Para hacer más sencillo la búsqueda e instalación de módulos, podemos elegir entre varias utilidades que, frecuentemente, se ven mezcladas en las documentaciones que podamos consultar, sin quedar claro cuál deberíamos utilizar en nuestro día a día.

En este artículo voy a aclarar estas utilidades, así como algunos trucos que podemos usar para crear entornos de trabajo aislados del resto.


##Instaladores de paquetes

-   **Distutils** era la herramienta estándar para empaquetar paquetes python.

	```
	  python setup.py install
	```

    Funciona bien, pero con algunas limitaciones que no eran fácil de arreglar. Viene de serie con la instalación de python y se puede reconocer por existir un fichero llamado `setup.py` que configura la creación del paquete listo para su distribución, pudiendo generar ficheros `.deb`  o `.rpm` para las distribuciones linux más populares, o los habituales instaladores para windows o mac a través de complementos. La instalación 

-   [**Setuptools**][12] era un proyecto que pretendía mejorar `distutils` añadiendo más funcionalidades.

	```
	  easy_install <module>
	```

    En muchos sentidos, se considera un *"estándar de facto"* gracias al comando [`easy_install`][11]; pero deja de funcionar en python3. Introdujeron el **egg** (huevo) como formato de los ficheros para distribuir módulos, así como un repositorio central llamado *"CheeseShop"* donde buscar los módulos a instalar que fue el germen de lo que ahora es el directorio [PyPi][]. Estos ficheros *eggs* suelen ser ficheros comprimidos que se instalan simplemente al ejecutarlos python como si fueran un programa.

-   [**Distribute**][13] es un *fork* de *setuptools* que pretendía acelerar su desarrollo y que lo ha suplantado en muchos casos. Su desarrollo ha quedado algo parado al salir *distutils2*.

-   Instalador [**pip**][pip]: es un popular instalador de uso similar a los instaladores de paquetes de las distribuciones linux.

	```
	  pip install <paquete>
	```

    Añade muchas funcionalidades como son las búsquedas de paquetes o la descarga de dependencias. Puede funcionar sobre setuptools, aunque lo normal es usarlo con distribute.

-   **Distutils2** (renombrado como **`packaging`** en python3.3+) es un fork de *distutils* que incorpora ideas traídas de *setuptools* y *distribute* y que se discuten mediante los PEPs habituales. Su instalador está inspirado por "pip" y será estándar para python3.


[11]: http://packages.python.org/distribute/easy_install.html "Easy_install"
[12]: http://pypi.python.org/pypi/setuptools "Setuptools (con instrucciones de instalación)"
[13]: http://pypi.python.org/pypi/distribute "Distribute (con instrucciones de instalación)"
[pip]: http://www.pip-installer.org/en/latest/index.html "Instalador pip"
[PyPi]: http://pypi.python.org/pypi "the Python Package Index"


##Instalador PIP

Centrémonos en la utilidad de instalación [`pip`][pip]. Se trata de una herramienta que puede buscar, instalar/desinstalar, reempaquetar,... y muchas más cosas que nos va a facilitar la vida a la hora de realizar instalaciones distribuidas como veremos a continuación.

Características de pip:

- Búsquedas en el repositorio [PyPi][]

- Descarga de todas las dependencias antes de la instalación. Muy importante para mantener la fidelidad de la instalación en despliegues remotos.

- Puede instalar directamente de una dirección de internet, o directamente desde sistemas de control de versiones como git, mercurial, subversion o bazaar.

- Con el comando `freeze` podemos crear un fichero de requisitos con la lista de los paquetes y su versión exacta que actualmente tenemos instalados.

- Con el comando `bundle` podemos crear *pybundles*, archivos que contienen múltiples paquetes.


##Virtualenv

Otra gran característica de **pip** es que funciona tremendamente bien con [virtualenv][]. No en vano, son del mismo autor, [Ian Bicking][1]. Virtualenv nos permitirá crear entornos de desarrollo aislados del resto de instalaciones python, controlando tanto las versiones de los módulos instalados como la versión de python que usaremos en él.

Pero creo que será mejor poner algunos ejemplos de las aplicaciones de virtualenv:

```bash
$ virtualenv --no-site-packages --python=/usr/bin/python3 py3
$ cd py3
$ source bin/activate
(py3)$ pip install markdown
```

Con estas líneas hemos conseguido instalar el módulo `markdown` en un entorno python3. El intérprete de python3 que ejecutaremos desde aquí estará instalado en la ruta `py3/bin/python` y el módulo márkdown en `py3/lib/python-3.2/site-packages`. También se ha instalado en `py3/bin/python` el script `markdown_py` que ejecutará el comando. En resumen, de una manera simple tenemos un entorno con lo mínimo donde hacer nuestras pruebas sin trastocar nada del sistema.

```bash
$ virtualenv --python=/usr/local/bin/jython jydjango
$ cd jydjango
$ source bin/activate
(jydjango)$ pip install django
(jydjango)$ django-admin.py startproject djython
(jydjango)$ cd djython/
(jydjango)$ jython manage.py runserver
Validating models...

0 errors found
Django version 1.4, using settings 'djython.settings'
Development server is running at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

En este caso, a partir de una instalación local de jython hemos creado un entorno virtual, en el que hemos instalado `django` y lo hemos ejecutado con jython. De este modo podemos experimentar con django y jython sin que afecte a cualquier otra instalación de django que tengamos.

A partir de aquí, la imaginación es el límite.

Como recomendación, instala [virtualenvwrapper][2], una colección de comandos para bash que hace más sencillo el uso de virtualenv, además de gestionar todos los entornos virtuales  desde un único directorio (`$HOME/.virtualenv`). También existe una [versión para PowerShell][3] para windows.



[virtualenv]: http://www.virtualenv.org "Virtuaenv"
[1]: http://blog.ianbicking.org/ "blog de Ian Bicking"
[2]: http://www.doughellmann.com/projects/virtualenvwrapper/
[3]: https://bitbucket.org/guillermooo/virtualenvwrapper-powershell
