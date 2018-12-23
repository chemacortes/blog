Title: Instalación cx_Oracle para ia64
Date: 2011-06-04 13:47
Author: Chema Cortés
Category: Python
Tags: howto, ia64, oracle, tip
Slug: instalacion-cx_oracle-para-ia64

#Itanium, un sistema ¿obsoleto?

Últimamente, algunos *grandes* de la informática como Microsoft, Oracle y RedHat han determinado que los sistemas Itanium han quedado obsoletos con lo que dejarán de darles soporte, aunque hace sólo unos pocos años estos sistemas de 64bits se ofertaban al mercado como el futuro de los sistemas servidores empresariales.

En este punto, me encuentro que tengo en mi trabajo algunos servidores Itanium II que, lejos de considerarlos obsoletos, me parecen perfectos para alojar en ellos algunos de los proyectos python desarrollados en plone o django. Con la reciente salida de la distribución Debian *"Squeeze"*, y con la ayuda de un alumno que vino a hacer sus prácticas con nosotros, me animé a sustituir el Linux RedHat que se había quedado sin mantenimiento por una la última versión *ia64* de debian. Esta versión es algo más limitada en paquetes que las versiones para arquitecturas i686 y amd64, pero con un poco de esfuerzo es posible completar la instalación compilando paquetes a partir de los fuentes. Y puedo afirmar que ha sido todo un éxito. Vuelvo a tener un sistema potente, completo y, sobre todo, mucho más libre.

La idea de este artículo es contar cómo instalar y configurar, en debian para itanium, del cliente de oracle y el conector `cx_Oracle` para python. 


#Instalación cliente oracle

Lo primero es descargar desde la [web de oracle][OCI] del cliente. Para ello hay que descargar los siguiente paquetes para itanium, previo registro gratuito:

	basic-10.2.0.4.0-linux-ia64.zip
	sdk-10.2.0.4.0-linux-ia64.zip
	sqlplus-10.2.0.4.0-linux-ia64.zip

	jdbc-10.2.0.4.0-linux-ia64.zip
	odbc-10.2.0.4.0-linux-ia64.zip

Los dos últimos son opcionales, pero siempre pueden venir bien guardarlos por si hacen falta en el futuro con alguna aplicación (el conector jdbc nos vendrá bien para usarlo con jython).

Se decomprimen estos paquetes en el mismo directorio y obtendremos un único directorio llamado:

	instantclient_10_2

Movemos este directorio a un lugar adecuado, por ejemplo a:

	/opt/oracle/instantclient_10_2

No olvidar darle permisos adecuados, sobre todo si queremos que el servidor apache (`mod_wsgi`) pueda acceder a él (puedo asegurar que se pierde mucho tiempo hasta que averiguas este fallo tan tonto):

    # chmod +rx /opt/oracle/instantclient_10_2/

[OCI]: http://www.oracle.com/technology/software/tech/oci/instantclient/htdocs/linuxsoft.html "Oracle Client Instant"


Cuando pasemos a compilar `cx_Oracle`, veremos algunos fallos por no ser capaz de encontrar algunas librerías compatidas. Para evitarlo, debemos crear algunos enlaces:

	# cd /opt/oracle
	# ln -s libclntsh.so.10.1 libclntsh.so
	# ln -s libclntsh.so.10.1 libclntsh.dylib


Ahora tenemos que actualizar las referencias a la libreras compartidas. Creamos el fichero `/etc/ld.so.conf.d/oracle.conf` con la siguiente línea:

	/opt/oracle/instantclient_10_2

Y actualizamos:

	# ldconfig

Para comprobar que funciona bien, podemos probar la utilidad `sqlplus` a ver si conectamos. Esta utilidad viene dentro del directorio.


Para poder compilar el paquete `cx_Oracle` se necesita unas cuantas variables de entorno que meteremos en el `.profile`:

```bash
export ORACLE_HOME="/opt/oracle/instantclient_10_2"
export DYLD_LIBRARY_PATH="$ORACLE_HOME"
export SQLPATH="$ORACLE_HOME"

export PATH="$PATH:$ORACLE_HOME"
```

Para instalar el paquete `cx_Oracle`, podemos instalar antes el paquete `python-pip` que nos ofrece la utilidad `pip` que nos hará más fácil la instalación:

    # apt-get install python-pip
    # pip install cx_Oracle


Con ésto se debería descargar, compilar e instalar `cx_Oracle`. Saldrán algunas advertencias que podemos ignorar. Si todo ha salido bien, podemos pasar a probar si podemos importar el módulo:

```text
# python
Python 2.6.6 (r266:84292, Dec 27 2010, 21:05:55)
[GCC 4.4.5] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import cx_Oracle
>>>
```

Con el módulo instalado, lo he probado desde el *"backend"* de oracle para django y todo funciona a la perfección.
