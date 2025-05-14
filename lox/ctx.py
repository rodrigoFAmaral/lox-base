from time import time
from types import MappingProxyType
from typing import TYPE_CHECKING, MutableMapping, TypeVar, cast


if TYPE_CHECKING:
    from .ast import Value

T = TypeVar("T")

builtins = cast(dict[str, "Value"], MappingProxyType({"clock": time, "super": super}))
ScopeDict = dict[str, "Value"]


class Ctx(MutableMapping[str, "Value"]):
    """
    Contexto de execução. Por enquanto é só um dicionário que armazena nomes
    das variáveis e seus respectivos valores.
    """

    @classmethod
    def from_dict(cls, env: dict[str, "Value"]) -> "Ctx":
        """
        Cria um novo contexto a partir de um dicionário.
        """
        new = cls()
        new.update(env)
        return new
