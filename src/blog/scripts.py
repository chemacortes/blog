import shutil
from os import environ
from pathlib import Path

# from subprocess import check_call

VENV = Path(environ["VIRTUAL_ENV"])
CWD = Path(__file__).parent


def remove_slimit_warning() -> None:
    """
    Quitar avisos de `slimit` diciendo que las tablas no están actualizadas.
    Se borran las tablas para que las recree.

    ./site-packages/slimit/yacctab.py
    ./site-packages/slimit/lextab.py
    """
    for tab in VENV.glob("./lib/python3.*/site-packages/slimit/*tab.py"):
        tab.unlink()
        print(f"Borrado {tab}")


def install_lexer_coconut() -> None:
    """
    Al instalar coconut se instala un lexer para pygments que no está
    actualizado. Como en el blog se usa bloques de código coconut en markdown,
    da error al generar el blog.

    Este script copia el lexer de coconut corregido dentro de los lexers de
    pygments. No es necesario tener instalado coconut.
    """

    lexers = VENV.glob("./lib/python3.*/site-packages/pygments/lexers")
    dest = next(lexers, None)
    if dest is None:
        print("### ERROR: no encontrado directorio lexers en módulo pygments")
    else:
        lexer = dest / "coconut.py"
        shutil.copyfile(CWD / "coconut-lexer.py", lexer)
        print(f"Lexer instalado: {lexer}")
