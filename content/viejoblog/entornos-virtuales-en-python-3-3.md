Title: Entornos virtuales en python 3.3
Date: 2012-10-23 20:58
Author: Chema Cortés
Category: Python
Slug: entornos-virtuales-en-python-3-3

Con la [nueva versión de python 3.3][3.3] se ha incorporado la propuesta [PEP-405][pep405] que añade al repertorio interno de python la posibilidad de crear entornos virtuales de modo parecido a virtualenv (vimos esta herramienta hace poco al hablar de la [instalación de módulos][1].

Tal como lo define [PEP-405][pep405]: *"Los *entornos virtuales* poseen su propio conjunto de paquetes instalados localmente, segregados del resto de paquetes instalados del sistema"*. Para crear y administrar estos entornos virtuales, se incluye el módulo `venv`, así como el script `pyvenv.py`.

Para crear un entorno virtual se puede utilizar el script `pyvenv` (con python 3.3):

```bash
$ pyvenv /ruta/al/nuevo/entorno/virtual
```

En windows, probablemente haya que ejecutar el script que se encuentra en `"C:\> Python33\Tools\Scripts\pyvenv.py"`. Posiblemente sea más sencillo ejecutar directamente el módulo `venv`:

```bash
$ python -m venv /ruta/al/nuevo/entorno/virtual
```

Entrando dentro del nuevo directorio, activamos el entorno de modo similar a como hacíamos con `virtualenv`:

```bash
$ cd /ruta/al/nuevo/entorno/virtual
$ source bin/activate
```

Hay que notar que el script `activate` se debe ejecutar con `source` ya que necesita cambiar algunas variables del entorno de ejecución actual. 

En windows, se debe ejecutar el script `Scripts\activate.bat`.

```powershell
C:\> cd entorno_virtual
C:\> Scripts\activate.bat
```

Una vez activado el entorno veremos que el prompt de la línea de comandos ha cambiado para indicarnos que estamos dentro. Las variables de entorno han cambiado, como puedes comprobar si miras `$PATH`. A partir de aquí, la instalación de paquetes con `easy_install` o `pip` se realizarán dentro del entorno. A diferencia con `virtualenv`, el módulo `venv` no instala en nuestro entorno ninguna de estas herramientas, por lo que lo primero que tendremos que hacer será instalarlas:

```bash
(py3.3) $ curl -O http://python-distribute.org/distribute_setup.py
(py3.3) $ python distribute_setup.py
(py3.3) $ easy_install pip
```

Para desactivar el entorno se ejecuta `deactivate`.

Aunque `venv` sigue el mismo funcionamiento que `virtualenv`, tiene notables carencias:

- No permite configurar versiones distintas de python

- No replica la instalación python del sistema en la copia local

- No permite independizar el entorno virtual del la ruta donde se crea (*no relocatable*)

En definitiva, los entornos virtuales creados con `venv` no son completamente independientes de la instalación python del sistema como sí puede hacer `virtualenv`. Esperemos que se amplien las opciones con nuevas versiones de python. De momento, seguiremos con `virtualenv`.



[3.3]: http://docs.python.org/3.3/whatsnew/3.3.html "What's new in python 3.3?"
[pep405]: http://www.python.org/dev/peps/pep-0405 "PEP-0405 Python Virtual Environments"

[1]: {filename}instalacion-de-modulos.md
[virtualenv]: http://www.virtualenv.org/ "Virtualenv"
