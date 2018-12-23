Title: BOM - marcas de orden de bytes
Date: 2012-07-10 13:32
Author: Chema Cortés
Category: Python
Tags: code, unicode
Slug: bom-marcas-de-orden-de-bytes

Los BOM's son marcas que aparecen en ficheros y transmisiones de datos para indicar el *"orden de los bytes"* de la codificación empleada. Si pensamos que el tamaño de cada dato transmitido puede ser 2, 4 u 8 bytes (16bits, 32 bits ó 64 bits), el orden de los bytes nos indica cómo se están empaquetando los bytes en cada dato.

Sin entrar en detalle, cuando usamos las codificaciones para unicode en ficheros, se suele convenir en el uso de una marca BOM al inicio del fichero para indicar el orden de los bytes del fichero, pero que sirve asimismo para saber la codificación empleada.

En unicode, el carácter BOM se representa por **U+FEFF**. Codificado en los distintos UTFs tenemos:

```python
# UTF-8
BOM_UTF8 = '\xef\xbb\xbf'

# UTF-16, little endian
BOM_LE = BOM_UTF16_LE = '\xff\xfe'

# UTF-16, big endian
BOM_BE = BOM_UTF16_BE = '\xfe\xff'

# UTF-32, little endian
BOM_UTF32_LE = '\xff\xfe\x00\x00'

# UTF-32, big endian
BOM_UTF32_BE = '\x00\x00\xfe\xff'
```

<sub>Extraído del fichero `codecs.py` de la librería estándar de python</sub>

Como la marca BOM se codifica de manera diferente según el sistema de codificación, podemos deducir qué codificación esta usando el fichero a partir de los 4 primeros bytes. De esta manera, muchos editores son capaces de emplear la codificación correcta.

Por otro lado, puede que sepamos qué codificación usan nuestros ficheros, pero en cambio nos molesta esos caracteres de más al inicio del fichero. En este caso, el módulo `codecs` de python nos facilita mucho la tarea. Basta emplear las siguiente codificaciones genéricas:

- `'utf-8-sig'` para UTF-8
- `'utf-16'` para UTF-16LE y UTF-16BE
- `'utf-32'` para UTF-32LE y UTF-32BE

Se introdujo `'utf-8-sig`' para no provocar incompatibilidades con el código existente que ya usaba `'utf-8`'. Usando estas codificaciones, el módulo `'codecs'` es suficientemente inteligente para quitar el BOM al leer el fichero, y para añadir el BOM al escribir, de modo completamente transparente.

Por ejemplo, estos días necesitaba pasar un fichero en `UTF-16LE` a `UTF-8`. Lo conseguí con el siguiente script:

```python
>>> import codecs
>>> f=codecs.open("fichero-utf16le.txt",encoding="utf-16")
>>> o=codecs.open("fichero-utf8.txt","wb",encoding="utf-8-sig")
>>> o.write(f.read())
>>> o.close()
```

O, completando [otro articulo][1], se podría hacer todo en una sóla línea:

```bash
$ python -c "import sys,codecs;codecs.EncodedFile(sys.stdout,'utf-16','utf-8-sig').writelines(sys.stdin)" <fichero_entrada.txt >fichero_salida.txt
```

Hay que tener en cuenta que el comando `iconv`, normalmente usado para convertir codificaciones de ficheros, no tiene en consideración el BOM. Con python tenemos una solución perfecta.


[1]: {filename}iconv-en-python.md
*[BOM]: Marca de orden de bytes
