Title: Último item de un iterable
Date: 2011-06-06 11:36
Author: Chema Cortés
Category: Python
Tags: tip
Slug: ultimo-item-de-un-iterable

Algunas veces necesitamos obtener el último item de un iterador. Para
ello se suele iterar hasta agotar el iterador:

```python
for it in iterador:
     pass

last_item = it  
```

Una alternativa que se ve bastante es convertir previamente el iterable
en una lista:

```python
last_item = list(iterador)[-1]
```

Tiene el incoveniente de gastar recursos inultilmente al crear una lista
de la que sólo nos interesa su último elemento.

En *[stackoverflow][1]* se pueden ver algunas [respuestas][2] a este
problema, pero ninguna me convence lo suficiente.

[1]: http://stackoverflow.com  
[2]: http://stackoverflow.com/questions/2138873/cleanest-way-to-get-last-item-from-python-iterator "Cleanest way to get last item from Python iterator"

Aquí pongo mi solución, simple y elegante donde las haya:

```python
last_item = max(enumerate(iterador))[1]
```

