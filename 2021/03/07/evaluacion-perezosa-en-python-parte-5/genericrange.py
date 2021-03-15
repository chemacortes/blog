from __future__ import annotations

from abc import abstractmethod
from collections.abc import Sequence
from functools import singledispatchmethod


class GenericRange(Sequence):
    def __init__(self, start=0, stop=None, step=1) -> None:
        if stop is None:
            start, stop = 0, start
        self._range = range(start, stop, step)

    @abstractmethod
    def getitem(self, pos: int) -> int:
        """
        Método abstracto.
          Función para calcular un elemento a partir de la posición
        """
        return pos

    @classmethod
    def from_range(cls: type[GenericRange], rng: range) -> GenericRange:
        """
        Constructor de un GenericRange a partir de un rango
        """
        instance = cls()
        instance._range = rng
        return instance

    def __len__(self) -> int:
        return len(self._range)

    @singledispatchmethod
    def __getitem__(self, idx):
        return NotImplemented

    @__getitem__.register
    def _(self, idx: int) -> int:
        i = self._range[idx]
        return self.getitem(i)

    def __repr__(self) -> str:
        classname = self.__class__.__name__
        r = self._range
        return f"{classname}({r.start}, {r.stop}, {r.step})"


@GenericRange.__getitem__.register
def __(self, idx: slice) -> GenericRange:
    i = self._range[idx]
    return self.from_range(i)
