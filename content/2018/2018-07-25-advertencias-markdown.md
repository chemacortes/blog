---
Title: Prueba de Advertencias
Date: 2018-07-24 23:55:53
Modified: 2019-04-07 21:06:04
Category: Técnicas
Tags: markdown
Slug:
Authors: Chema Cortés
Summary: Código Markdown para la extesión "admonition"
Lang: es
Translation: false
Status: draft
---

El formato general:

~~~ md
!!! type "optional explicit title within double quotes"
    Any number of other indented markdown elements.

    This is the second paragraph.
~~~

Por ejemplo, una advertencia sin tipo definido:

~~~ md
!!! Advertencia
    Ejemplo de una advertencia sin tipo.

    Segundo párrafo.

    Tercer párrafo.
~~~

Quedaría así:

!!! Advertencia
    Ejemplo de una advertencia sin tipo.

    Segundo párrafo.

    Tercer párrafo.

Advertencias de tipo: `update`, `hint`. `important` y `note`:

!!! tip
    Un truco...

Advertencias de tipo: `warning`, `attention`, `caution` y `danger`

!!! danger "Peligro"
    Una advertencia de tipo `danger` con título personalizado.
