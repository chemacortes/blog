Title: iconv en python
Date: 2011-08-04 18:38
Author: Chema Cortés
Category: Python
Tags: tip
Slug: iconv-en-python

Últimamente he necesitado pasar algunos ficheros de una web a codificación `utf-8`, codificación de caracteres más acorde con lo que se lleva hoy en día. En sistemas linux es una labor que se puede hacer fácilmente con la utilidad `iconv`:

```bash
$ iconv -f cp850 -t utf8 <fichero_entrada.txt >fichero_salida.txt
```

Pero hay veces que es necesario realizar esta conversión en windows. Si tenemos instalado `python`, una forma rápida de hacerlo sería:

```bash
$ python -c "import sys,codecs;codecs.EncodedFile(sys.stdout,'latin-1','utf-8').writelines(sys.stdin)" <fichero_entrada.txt >fichero_salida.txt
```

...¡y todo en una sóla línea![^1]

Tan sólo puntualizar que esta conversión emplea *iteradores*, por lo que no tiene que ser un problema el tamaño del fichero de texto a convertir.


[^1]: Para ver más ejemplos de *"one-liners"* os recomiendo este [artículo](http://joedicastro.com/python-one-liners-potencia-en-una-sola-linea.html)  de Joe di Castro
