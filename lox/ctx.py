from typing import TypeVar

T = TypeVar("T")

class Ctx(dict[str, T]):
    """
    Contexto de execução. Por enquanto é só um dicionário que armazena nomes 
    das variáveis e seus respectivos valores.
    """
