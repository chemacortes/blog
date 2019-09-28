---
Title: Manejo de rutas con pathlib
Date: 2019-09-28 17:53:57
Modified: 2019-09-28 17:56:08
Category: Python
Tags: python, pathlib
Slug: manejo-de-rutas-pathlib
Authors: Chema Cortés
Summary: Es difícil escribir un script de python que no interaccione con el sistema de ficheros de un modo u otro, por lo que python dispone de varios módulos para tal fin. El objeto `Path` viene a poner orden entre tantos módulos y funciones para manejo de ficheros. Se puede decir sin duda que usar `Path` se ha convertido en la forma más _pythónica_ de manipular ficheros y directorios.
Lang: es
Translation: false
Status:
---

Es difícil escribir un script de python que no interaccione con el sistema de ficheros de un modo u otro, por lo que python dispone de varios módulos para tal fin: `os`, `os.path` (_submódulo de os_), `shutil`, `stats`, `glob`,...En la intención estaba ser multiplataforma, lo que ha sido fuente de muchos mayores quebraderos de cabeza con las distintas codificaciones de caracteres y distintas formas de expresar rutas de ficheros que existen.

El objeto `Path` viene a poner orden entre tantos módulos y funciones para manejo de ficheros. La librería estándar se ha reescrito para aceptar estos objetos `Path`. Se puede decir sin duda que usar `Path` se ha convertido en la forma más _pythónica_ de manipular ficheros y directorios.

Empecemos por un ejemplo traído de la [documentación oficial][pathlib]:

```python
>>> from pathlib import Path
>>> p = Path('/etc')
>>> q = p / 'init.d' / 'reboot'
>>> q
PosixPath('/etc/init.d/reboot')
>>> q.resolve()
PosixPath('/etc/rc.d/init.d/halt')
```

Paso por paso: importa el constructor `Path` del módulo `pathlib`. Con él construye un objeto con la ruta `/etc` y, usando el operador `/`, genera otro objeto que representa la ruta `/etc/init.d/reboot`. Automáticamente, estos objetos se construyen como instancias de `PosixPath`, que es una subclase especializada de `Path` para manejos de ficheros en sistemas Posix. La ruta `/etc/init.d/reboot` apunta a un _enlace simbólico_, por lo que se usa el método `resolve` para obtener la ruta absoluta del fichero al que apunta.

!!! Nota
    Observa que las operaciones con objetos _Path_ generan objetos _Path_ con lo que podemos encadenar operaciones para navegar a través de una jerarquía de directorios.

## Módulos a los que sustituye o no sustituye

Obviamtente, el módulo clásico `os.path`, utilizado para manipulación de rutas, es reemplazado totalmente por `pathlib`.

Del módulo `os` reemplaza muchas de sus funciones para manipular ficheros y directorios. Aún así, el módulo `os` contiene otras muchas funciones para el manejo de entornos o lanzamiento de procesos que no cambian. Así mismo, hay algunas operaciones especializadas con ficheros y directorios (eg: `os.walk`) que no han sido reempladas. De hecho son más eficientes que si se hicieran con objetos `Path`.

Otro módulo que ya no es necesario es `glob`, utilizado para buscar ficheros mediante patrones de búsqueda.

## Rutas puras y concretas

Según si tienen acceso al sistema de ficheros, podemos distingure entre:

- Ruta pura: rutas que no requieren acceso al sistema de ficheros (`PurePath`, `PurePosixPath`, `PureWindowsPath`)
- Ruta concreta: rutas con acceso al sistema de ficheros (`Path`, `PosixPath`, `WindowsPath`)

Las _rutas puras_ son superclases de las _rutas concretas_. Mejor verlo gráficamente como jerarquía de clases:

![Jerarquía de clases Path](/pictures/pathlib-inheritance.png)

## Ejemplos

Voy a poner algunos ejemplos de uso de `pathlib` para que compares con el modo como lo estabas haciendo hasta ahora. Recomiendo revisar la documentación del módulo [pathlib][] ante cualquier duda.

Para escribir en un fichero, usamos el método `open` de modo similar a como se hacía con la función `open` del mismo nombre:

```python
from pathlib import Path

path = Path('.config')
with path.open(mode='w') as config:
    config.write('# config goes here')
```

Si sólo vamos a escribir una línea, también se podría hacer de un modo más directo:

```python
Path('.config').write_text('# config goes here')
```

Pongamos un ejemplo más complejo: queremos localizar los scripts de python dentro de la carpeta `proyectos` que tengan una frase. Lo habitual para recorrer un directorio era usar alguna función como `os.walk` o `os.scandir` para ir navegando a través de la jerarquía de directorios e ir leyendo los ficheros python hasta localizar los que buscamos.

Veamos cómo se hace con `Path`:

```python
from pathlib import Path

proyectos = Path.home() / 'proyectos'  # carpeta en el directorio HOME
palabra = "pathlib"

ficheros = [p for p in proyectos.rglob("*.py")
            if palabra in p.read_text()]
```

Partimos del `Path.home()`, el directorio de usuario, y creamos la ruta del directorio `proyectos`. Invocando el método `.rglob()` obtenemos, recursivamente, todos los ficheros que cumplan con el patrón dado. Bastante simple.

La lista resultante es una lista de objetos _Path_, lo que nos facilita cualquier manipulación posterior que deseemos hacer sobre estos ficheros. Por ejemplo, vamos a calcular el tamaño total que ocupan:

```python
size = sum(p.stat().st_size for p ficheros)
```

Si se prefiere, se puede seguir usando el viejo `os.path.getsize`. Ahora también acepta objetos `Path`:

```python
import os.path

size = sum(os.path.getsize(p) for p ficheros)
```

[pathlib]: https://docs.python.org/3.7/library/pathlib.html "Documentación del módulo pathlib"
