# Blog ch3m4.org

Este es un blog más creado con [pelican][], un generador de sitios web estáticos
programado con python. Aunque es muy potente y fácil de usar, hay algunos
problemas y mejoras que he ido añadiendo, más allá de lo que sería la creación
del blog.

## Mejoras

### Extensiones recomendadas para vscode

Tanto la escritura de contenidos como la programación python, se realiza con
vscode. Las extensiones utilizadas se incluyen como "extensiones recomendadas"
que pueden verse al abrir el proyecto desde vscode.

Fichero: `.vscode/extensions.json`

### Plantilla

Los artículos nuevos se crean siguiendo una plantilla: `src/blog/template.md`.

Esta plantilla tiene varios campos:

- **TITLE**: título del artículo
- **CATEGORY**: categoría
- **AUTHOR**: autor (eg: Chema Cortés)
- **NOW**: fecha y hora actuales
- **SLUG**: título transformado para su uso en URIs.

Esta plantilla se puede autorellenar con el script `src/blog/new_article.py`
pasando como argumento el título y la categoría.

Para mayor facilidad, se ha creado una tarea de vscode que se invoca con **F6**
llamada **"new article"** que pedirá el título y la categoría a elegir entre
algunas disponibles.

La tarea está definida en `.vscode/tasks.json`

### Campo "Modified" automático

El campo **Modified** de un artículo cambia automáticamente cada vez que se
modifica el artículo. Esto se consigue con la extensión _"Auto Time Stamp"_
(`lpubsppop01.vscode-auto-timestamp`). También rellena el campo **Date** si está
vacío, por lo que basta borrarlo para que se ponga la fecha y hora actualizadas.

Opciones incluidas en `.vscode/settings.json`:

```json
{
  "lpubsppop01.autoTimeStamp.birthTimeStart": "[dD]ate *:",
  "lpubsppop01.autoTimeStamp.modifiedTimeStart": "[mM]odified *:",
  "lpubsppop01.autoTimeStamp.momentFormat": " YYYY-MM-DD HH:mm:ss",
}
```

## Problemas

Cada problema tiene un script que lo corrige y que puede ser invocado a través
de _poetry run_.

### Warnings de slimit

Al generar el sitio con pelican, hay veces que sale un error con el módulo
slimit. Este error se debe a que el lexer usa alguna tabla desactualizada. Basta
con borrar las tablas para que las regenere y así dejará de dar estos avisos.

Para borrar estas tablas:

```bash
$ poetry run slimit_warning
Borrado .venv/lib/python3.9/site-packages/slimit/lextab.py
Borrado .venv/lib/python3.9/site-packages/slimit/yacctab.py
```

### Problema con la sintaxis de coconut

En algún artículo se incluye código coconut. Para resaltar la sintáxis, markdown
usa pygments. El lenguaje coconut incorpora un lexer para pygments, pero no está
actualizado, con lo que provoca errores que para la generación del blog.

Para solucionarlo, se ha corregido el lexer que viene con coconut, por lo que es
necesario copiarlo en el módulo pygments que hay en el entorno virtual
(`.venv`).

Para instalar este lexer:

```bash
$ poetry run coconut_lexer
Lexer instalado: .venv/lib/python3.9/site-packages/pygments/lexers/coconut.py
```

No instalar `coconut` en este entorno virtual (al menos hasta que corrijan el
lexer)

[pelican]: https://getpelican.com/
