from abc import ABC
from typing import Any, Callable, Iterator
from functools import singledispatch
from types import BuiltinFunctionType, FunctionType, MethodDescriptorType, MethodType


class Node(ABC):
    """
    Classe base para todos os nós da árvore sintática.

    O módulo `abc` é usado para criar uma classe abstrata. Isso significa que
    não podemos instanciar essa classe diretamente. Em vez disso, devemos
    criar subclasses que implementem os métodos abstratos definidos aqui.
    """

    def eval(self, ctx):
        raise NotImplementedError("Método eval não implementado!")

    def pretty(self, indent: int = 2) -> str:
        """
        Método para imprimir a árvore sintática de forma legível.

        O parâmetro `indent` é usado para controlar a indentação da impressão.
        """
        parts = []
        for indent_level, line in self._pretty_lines():
            parts.append(indent * indent_level * " ")
            parts.append(line)
            parts.append("\n")
        return "".join(parts)

    def is_leaf(self) -> bool:
        """
        Método que verifica se o nó é uma folha na árvore sintática.

        Um nó é considerado uma folha se não tem filhos do tipo `Node`.
        """
        for name in self.__annotations__:
            value = getattr(self, name)
            if isinstance(value, (Node, list, tuple, dict)):
                return False
        return True

    def _pretty_lines(self, indent_level: int = 0) -> Iterator[tuple[int, str]]:
        """
        Método auxiliar para imprimir a árvore sintática de forma legível.

        O parâmetro `indent_level` é usado para controlar a indentação da impressão.
        """
        # Um pouquinho de Python avançado aqui.
        # O método `_pretty_lines` é um gerador. Cada yield retorna uma dupla com
        # o nível de indentação da linha e o conteúdo a ser impresso
        #
        # No caso simples, imprimimos a classe usando str(self). Fazemos isso se
        # a classe não tiver nenhum filho do tipo Node.
        if self.is_leaf():
            yield indent_level, str(self)
            return

        # No caso mais complexo, começamos com a linha de abertura, imprimindo
        # o nome da classe e um parêntese de abertura
        yield indent_level, str(self.__class__.__name__) + "("

        # O attributo "__annotations__" é um dicionário que contém os nomes dos
        # atributos declarados e seus tipos correspondentes. Vamos pegar os tipos
        # na ordem de declaração e imprimir o nome e valores correspondentes
        for attr in self.__annotations__:
            # attr é o nome do atributo. Obtemos o valor do atributo usando a
            # função `getattr` do Python
            value = getattr(self, attr)

            # Se o valor for um objeto do tipo `Node`, chamamos o método `pretty_lines`
            # recursivamente. Caso contrário, usamos a implementação genérica
            # do método `pretty`
            if not isinstance(value, Node):
                yield indent_level + 1, f"{attr}={pretty(value)}"
                continue

            lines = iter(value._pretty_lines(indent_level + 1))
            (_, first_line) = next(lines)

            # Tratamos a primeira linha de forma diferente, pois ela é prefixada
            # com o nome do atributo.
            yield indent_level + 1, f"{attr}={first_line}"

            # O comando "yield from" gera todos os valores remanescentes do
            # iterador `lines`.
            yield from lines

        # Terminamos fechando o parênteses que foi aberto na primeira linha
        yield indent_level, ")"

    def visit(self, visitors: dict[type, Callable[["Node"], Any]]) -> None:
        """
        Recebe um dicionário de tipos associados a funções.

        Executa a função correspondente ao tipo para cada nó na árvore sintática.
        """

        # Primeiro visitamos os filhos do nó atual.
        for name in self.__annotations__:
            value = getattr(self, name)
            if isinstance(value, Node):
                value.visit(visitors)

        # Agora visitamos self, se necessário
        for subtype in type(self).mro():
            try:
                visitor = visitors[subtype]
                visitor(self)
                break
            except KeyError:
                continue


@singledispatch
def pretty(obj: Any) -> str:
    """
    Função que imprime attributos da árvore sintática de forma legível.

    Aqui usamos o `singledispatch` para criar uma função genérica que pode
    ser chamada com diferentes implementações dependendo do tipo do primeiro
    argumento.

    A implementação genérica simplesmente pergunta se o objeto tem um método
    pretty e executa ele. Caso contrário, converte o objeto para string usando
    o método `repr` do Python.
    """
    if hasattr(obj, "pretty"):
        data = obj.pretty()
        if not isinstance(data, str):
            raise ValueError("O método pretty deve retornar uma string")
        return data

    return repr(obj)


# Implementação de `pretty` para argumentos do tipo Função
# Como se pode ver, existem vários tipos que representam funções de
# diferentes maneiras no Python.
@pretty.register(FunctionType)
@pretty.register(BuiltinFunctionType)
@pretty.register(MethodDescriptorType)
@pretty.register(MethodType)
def _(obj) -> str:
    """
    Implementação do método `pretty` para objetos do tipo `Node`.

    Aqui chamamos o método `pretty` da classe base `Node`.
    """
    return obj.__name__
