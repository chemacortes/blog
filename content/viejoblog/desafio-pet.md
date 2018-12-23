---
Title: Desafío PET1
Date: 2011-03-14 22:33
Modified: 2018-12-10 02:26:15
Author: Chema Cortés
Category: Python
Tags: code
Slug: desafio-pet
---

Hace mucho tiempo, el grupo de programadores [Python de
Argentina](http://python.org.ar) publicaron el primer número de la
revista [PET: Python Entre Todos](http://revista.python.org.ar)

En ese primer número se proponía el siguiente desafío PET:

> Escribir un programa que reciba un número en la entrada estándar e
> imprima por pantalla la factorización del número. Los siguientes
> ejemplos muestran posibles entradas y cómo se espera que sean las
> salidas.
>
```
	> entrada: 11
	>  salida: 11
	>
	> entrada: 8
	>  salida: 2^3
	>
	> entrada: 24
	>  salida: 2^3 x 3
	>
	> entrada: 168
	>  salida: 2^3 x 3 x 7
```
>  Notar que los factores se ordenan en orden creciente y si un factor
> aparece más de una vez, se debe expresar en forma de potencia. Los
> participantes deben enviar su solución como un archivo .py y esta será
> ejecutado con python 2.7. El ganador del desafío será aquel que logre
> la solución con la menor cantidad de caracteres.

Desconozco el motivo, pero a fecha de hoy todavía no se ha dado la
solución. El cuadro de honor de las mejores soluciones se puede ver
[aquí](http://python.org.ar/pyar/Proyectos/RevistaPythonComunidad/PET1/Desafio "Ranking")
donde (*¡Oh, sorpresa!*) estoy en cabeza.

Para todos los que estén aún esperando la solución de *111 caracteres*,
aquí va la mía:

~~~python
n=input();d=1;r=""
while d<n:
 d+=1;s=0
 while n%d<1:n/=d;s+=1
 if s:r+=" x %d"%d+"^%d"%s*(s>1)
print r[3:]or n
~~~

Para medir bien el número de caracteres, hay tener en cuenta que se
guarda con fin de línea estilo unix, sin EOF y sin tabuladores (se evita
tener dos espacios seguidos). Todavía espero una solución mejor. Si te
fijas, el *or* de la última línea está pegado con el primer argumento.
Es un truco muy sucio que no debería haberlo permitido el intérprete.

Aquí tienes el fichero para descargar:
[pet1-pych3m4.py]({static}/extra/pet1-pych3m4.py)
