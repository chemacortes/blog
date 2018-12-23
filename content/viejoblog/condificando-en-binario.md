Title: Codificando en binario
Date: 2012-01-26 20:24
Author: Chema Cortés
Category: Python
Tags: tip, unicode
Slug: condificando-en-binario

A raiz de la consulta de un colega, me ha llamado la atención el módulo `binascii`. Este módulo se encarga de la codificación y decodificación de cadenas binarias para su transmisión en mensajes de texto. Lo habitual es que sea usado por otros módulos como `uu`, `base64` o `binhex`, por lo que no es nada frecuente ver su uso directo en una aplicación.

Sin embargo, `binascii` posee algunas funciones que pueden sernos bastante útiles a la hora de simplificar el empaquetado de datos que requieren determinadas APIs, en lugar de usar estructuras más complejas como `array` o `struct`. También se revela muy útil a la hora de crear batería de tests donde necesitemos chequear valores binarios.

## Estructuras array y struct

Por ejemplo, imaginemos que nuestra API nos pide que empaquetemos un número entero como cuatro bytes. Antes de python3 no existía una forma para controlar el tamaño en bytes de un objeto sin tener que recurrir a alguna estructura especializada. Por ejemplo:

```python
from array import array

def numpack(num):
    a=array('L')
    a.append(num)
    return a.tostring()[::-1]

n=numpack(0xffeeddcc)  # res: \xff\xee\xdd\xcc
```

En el resultado final ha hecho falta invertir el orden de los bytes debido a que nos estaba usando un orden *"little-endian"* para su codificación. El orden puede depender del sistema donde estemos trabajando, con lo que no es nada seguro usar este método. Es preferible el uso más especializado de `struct` donde tendremos algo más de control sobre éste y muchos otros aspectos:

```python
from struct import pack

def numpack(num):
    return pack('!L', num)

n=numpack(0xffeeddcc)  # res: \xff\xee\xdd\xcc
```

Nota que en la cadena de formato que se pasa a `pack()` tiene un indicador `'!'` al principio, con el que indicamos que queremos una ordenación *"network (=big-endian)"*.

El proceso inverso es tan fácil como usar la función complementaria `unpack`:

```python
unpack('!L', n)[0]
```


## Codificando mensajes

Lo visto hasta ahora funciona bien cuando tenemos que interaccionar con una API que use tamaños fijos para los datos. Pero, ¿qué pasa cuando los datos son de longitud variable, por ejemplo, un mensaje largo de decenas de bytes? En el mejor de los casos, tendríamos que ir byte a byte, tal vez apoyándonos en `array` o `struct` para realizar las conversiones, algo a todas luces resulta bastante tedioso.

Como ya adelanté, el módulo `binascii` nos va a ayudar en este cometido, en concreto la función `b2a_hex` y su contraparte `a2b_hex`.

Por ejemplo, nos envían en un mensaje un entero codificado en multibyte. No sabemos si son 2, 4 u 8 bytes, o incluso podrían ser más bytes de tratarse de un `BigInt` (entero muy largo). Con `binascii` podríamos resolverlo así:

```python
from binascii import b2a_hex, a2b_hex

num = int(b2a_hex(msg), 16)
```

Para el proceso contrario, codificar un entero en una cadena binaria, usaríamos `a2b_hex`:

```python
h = "%x"%num
if len(h)%2 == 1:
    h = "0" + h

msg = a2b_hex(h)
```

Hemos tenido cuidado de que la cadena hexadecimal tenga longitud par ya que `a2b_hex` codifica siempre cada byte a partir de una pareja de dígitos hexadecimales.

## Estudio codificaciones unicode

También es posible usar `binascii` para estudiar las codificaciones de cadenas unicode, lo que hace más sencillo crear tests automáticos para funciones que empleen unicode. Sin muchos adornos, haríamos algo así:

```python
#-*- coding: utf-8 -*-

from binascii import b2a_hex, a2b_hex

cadena = u"Peón \N{BLACK CHESS PAWN}"

print b2a_hex(cadena.encode('utf-8'))

#res: 5065c3b36e20e2999f
```

Comparando el resultado obtenido con la cadena unicode, vemos que la *ó* acentuada se codifica en 'utf-8' como `0xc3b3`, o que la figura de peón negro se codifica como `0xe2999f`.

Si cambiamos la codificación por 'utf-16' obtenermos como resultado `fffe50006500f3006e0020005f26`. Además de ser más larga, vemos que se añade al principio `fffe`, que es lo que se denomina BOM, y que nos indica qué ordenación de bytes se ha usado en la codificación (`'FEFF'` para *Big Endian* / `'FFFE'` para *Little Endian*). Con `fffe` nos indica concretamente que se ha usado la codificación 'UTF-16 Little Endian', con lo que tenemos los bytes invertidos para cada caracter codificado (ver más info en el [artículo sobre BOM][1] de la wikipedia).

De no desear que se nos añada la marca BOM, podríamos haber forzado la codificación mediante `'utf-16be'` ó `'utf-16le'` para *Big Endian* y *Little Endian*, respectivamente.


[1]: http://es.wikipedia.org/wiki/Marca_de_orden_de_bytes_(BOM)

*[BOM]: Byte Order Mark
