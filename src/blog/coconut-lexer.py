#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------------------------------------------------
# INFO:
# -----------------------------------------------------------------------------------------------------------------------

"""
Author: Evan Hubinger
License: Apache 2.0
Description: Syntax highlighting for Coconut code.

Patch: 2021-02-04 Chema Cortés
"""

# -----------------------------------------------------------------------------------------------------------------------
# IMPORTS:
# ----------------------------------------------------------------------------------------------------------------------

from __future__ import absolute_import, division, print_function, unicode_literals

from coconut.root import *  # NOQA
from pygments.lexer import bygroups, words
from pygments.lexers import PythonConsoleLexer, PythonLexer
from pygments.token import Keyword, Name, Number, Operator, Text
from pygments.util import shebang_matches

__all__ = [
    "CoconutPythonLexer",
    "CoconutPythonConsoleLexer",
    "CoconutLexer",
]

from coconut.constants import (
    coconut_specific_builtins,
    code_exts,
    default_encoding,
    magic_methods,
    new_operators,
    reserved_vars,
    shebang_regex,
    tabideal,
    template_ext,
)

# -----------------------------------------------------------------------------------------------------------------------
# LEXERS:
# -----------------------------------------------------------------------------------------------------------------------


def lenient_add_filter(self, *args, **kwargs):
    """Disables the raiseonerror filter."""
    if args and args[0] != "raiseonerror":
        self.original_add_filter(*args, **kwargs)


class CoconutPythonLexer(PythonLexer):
    """Coconut-style Python syntax highlighter."""

    name = "coconut_python"
    aliases = ["coconut_python", "coconut_py", "coconut_python3", "coconut_py3"]
    filenames = ["*" + template_ext]

    def __init__(
        self,
        stripnl=False,
        stripall=False,
        ensurenl=True,
        tabsize=tabideal,
        encoding=default_encoding,
        **options  # 2021-02-04 patch
    ):
        """Initialize the Python syntax highlighter."""
        PythonLexer.__init__(
            self,
            stripnl=stripnl,
            stripall=stripall,
            ensurenl=ensurenl,
            tabsize=tabsize,
            encoding=default_encoding,
            **options  # 2021-02-04 patch
        )
        self.original_add_filter, self.add_filter = (
            self.add_filter,
            lenient_add_filter,
        )


class CoconutPythonConsoleLexer(PythonConsoleLexer):
    """Coconut-style Python console syntax highlighter."""

    name = "coconut_pycon"
    aliases = ["coconut_pycon", "coconut_pycon3"]
    filenames = []

    def __init__(
        self,
        stripnl=False,
        stripall=False,
        ensurenl=True,
        tabsize=tabideal,
        encoding=default_encoding,
        python3=True,
        **options  # 2021-02-04 patch
    ):
        """Initialize the Python console syntax highlighter."""
        PythonConsoleLexer.__init__(
            self,
            stripnl=stripnl,
            stripall=stripall,
            ensurenl=ensurenl,
            tabsize=tabsize,
            encoding=default_encoding,
            python3=python3,
            **options  # 2021-02-04 patch
        )
        (self.original_add_filter, self.add_filter) = (
            self.add_filter,
            lenient_add_filter,
        )


class CoconutLexer(PythonLexer):
    """Coconut syntax highlighter."""

    name = "coconut"
    aliases = ["coconut", "coco", "coc"]
    filenames = ["*" + ext for ext in code_exts]

    tokens = PythonLexer.tokens.copy()
    tokens["root"] = [
        (r"|".join(new_operators), Operator),
        (
            r"(?<!\\)(match)?((?:\s|\\\s)+)(data)((?:\s|\\\s)+)",
            bygroups(Keyword, Text, Keyword, Text),
            py_str("classname"),
        ),
        (r"def(?=\s*\()", Keyword),
    ] + tokens["root"]
    tokens["keywords"] += [
        (words(reserved_vars, prefix=r"(?<!\\)", suffix=r"\b"), Keyword),
    ]
    tokens["builtins"] += [
        (words(coconut_specific_builtins, suffix=r"\b"), Name.Builtin),
        (r"MatchError\b", Name.Exception),
    ]
    tokens["numbers"] = [
        (r"0b[01_]+", Number.Integer),
        (r"0o[0-7_]+", Number.Integer),
        (r"0x[\da-fA-F_]+", Number.Integer),
        (r"\d[\d_]*(\.\d[\d_]*)?((e|E)[\d_]+)?(j|J)?", Number.Integer),
    ] + tokens["numbers"]
    tokens["magicfuncs"] += [
        (words(magic_methods, suffix=r"\b"), Name.Function.Magic),
    ]

    def __init__(
        self,
        stripnl=False,
        stripall=False,
        ensurenl=True,
        tabsize=tabideal,
        encoding=default_encoding,
        **options  # 2021-02-04 patch
    ):
        """Initialize the Python syntax highlighter."""
        PythonLexer.__init__(
            self,
            stripnl=stripnl,
            stripall=stripall,
            ensurenl=ensurenl,
            tabsize=tabsize,
            encoding=default_encoding,
            **options  # 2021-02-04 patch
        )
        self.original_add_filter, self.add_filter = self.add_filter, lenient_add_filter

    def analyse_text(text):
        return shebang_matches(text, shebang_regex)
