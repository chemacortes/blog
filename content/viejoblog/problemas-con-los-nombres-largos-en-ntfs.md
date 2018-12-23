Title: Problemas con los nombres largos en NTFS
Date: 2012-04-04 13:07
Author: Chema Cortés
Category: Python
Tags: ntfs, windows
Slug: problemas-con-los-nombres-largos-en-ntfs

Un buen día comenté a un compañero de trabajo que en su carpeta compartida del servidor de ficheros pronto iba a tener problemas al usar nombres de carpetas demasiado largos. El explorador de ficheros ya se negaba a listas algunas carpetas y el problema iba a más con algunas herramientas (backups, antivirus,...).

La respuesta fue una pregunta: *¿Sería posible sacar un listado de todos los ficheros con ruta absoluta demasiado larga?*

Después de dudar un rato (y comprobar que el comando `dir` no era válido para esta labor) , me decidí a averiguar si python sería capaza de realizar dicha tarea. Éste es el resultado de ése estudio.

##Problema con los nombres largos

Resulta bastante chocante que la API de windows limite la máxima longitud para una ruta al valor de **MAX_PATH**, definido como 260 caracteres. Se trata únicamente de una limitación en la API, ya que el kernel de windows está preparado para manejar rutas muchísimo más largas. Como consecuencia, muchas aplicaciones fallan con rutas largas, desde los comandos de terminal hasta las utilidades gráficas del sistema.

Para evitar en parte este problema, podemos usar en nuestras aplicaciones las versiones *unicode* de las funciones *ANSI* de la API. Estas versiones unicode admiten como parámetros rutas de hasta 32.767 caracteres, suficientemente largas para un uso normal.

En en caso de la librería estándar de python, el módulo `os.path` (sinónimo de `os.ntpath` en windows) tiene buena cuenta de qué API invocar, según sea el caso. De un modo transparente, **con sólo codificar las rutas en unicode evitaremos la limitación `MAX_PATH` en la longitud de las rutas**.

##Codificación de rutas extendida

Además de codificar las rutas en unicode, tenemos que indicar que se trata de una *ruta extendida* añadiendo el prefijo `'\\?\'` a una ruta absoluta. Por ejemplo, `"\\?\D:\ruta\muy\muy\larga"`. Como gran limitación, no se puede usar esta nomenclatura con rutas relativas, por lo que las rutas relativas siempre estarán limitadas a `MAX_PATH` como máxima longitud.

Es posible, también, indicar una ruta UNC (*Universal Naming Convention*) como *ruta extendida* como `\\?\server\share`, donde `server` sería el nombre del servidor y `share` el nombre de la carpeta compartida.

Para más información sobre las rutas extendidas, visitar la página web [Naming Files, Paths, and Namespaces][1] de MSDN.

##Script para listar ficheros de nombres muy largos

Por último, sólo queda lo más fácil: codificar el script ;-)

Es común que la codificación que lleva por defecto la cónsola de comandos falle con las cadenas unicode. Si pensamos sacar por cónsola los nombres de ficheros, lo recomendable es cambiar la codificación por una más apropiada, como la `cp1252`, lo más aproximado a `utf-8` que podemos encontrar:

        C:\> chcp 1252

Para hacer nuestro script, podríamos haber usado cualquiera de las funciones `os.walk` de la librería estándar; pero, no sé porqué, fallan a crear la lista de directorios. Ésto nos obliga a crear nuestro propio método para recorrer la jerarquía de directorios.

Por comodidad, voy a lanzar el script en una máquina distinta de la que hace de servidor de ficheros ya que no dispongo de python en los servidores. Usaré la nomenclatura UNC para identificar los recursos compartidos.

```python
#-*- coding: utf-8 -*-

import os

MAX_PATH=260

def longnames(dirpath):
    """Iterador que devuelve las rutas largas (>=MAX_PATH)"""
    
    #Hay que forzar unicode para evitar el límite MAX_PATH
    dirpath=unicode(dirpath)
    if not dirpath.endswith("\\"):
        dirpath+="\\"

    dirs=[]
    
    for f in os.listdir(dirpath):
        
        name = dirpath+f
        
        if len(name)>=MAX_PATH:
            yield name

        #poblar la lista de directorios
        #para recorrer en orden
        if os.path.isdir(name):
            dirs.append(name)

    for d in dirs:
        for f in longnames(d):
            yield f

def listshare(server, share):
    """Crea un UNC para el recurso compartido.
       Devuelve un iterador para las rutas largas (>=MAX_PATH)
    """    
    dirpath=r"\\?\UNC\%s\%s"%(server, share)
    return longnames(dirpath)

```

Su uso simple podía ser:

```python
#-*- coding: utf-8 -*-

import codecs

#PARÁMETROS
SERVER="MiServidor"
SHARE=r"Usuario\dir1"

fOut=codecs.open("longnames.txt", "w", encoding="utf-8")

for name in listshare(SERVER,SHARE):
    
    print name
    print >>fOut, name.replace(DIRPATH,".\\")
    
fOut.close()
```

*[UNC]: Universal Naming Convention

[1]: http://msdn.microsoft.com/en-us/library/windows/desktop/aa365247%28v=vs.85%29.aspx "Naming Files, Paths, and Namespaces"
