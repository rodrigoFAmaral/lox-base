"""
Implementa o transformador da árvore sintática que converte entre as representações

    lark.Tree -> lox.ast.Node.

A resolução de vários exercícios requer a modificação ou implementação de vários
métodos desta classe.
"""

from typing import Callable
from lark import Transformer, v_args

from . import runtime as op
from .ast import *


def op_handler(op: Callable):
    """
    Fábrica de métodos que lidam com operações binárias na árvore sintática.

    Recebe a função que implementa a operação em tempo de execução.
    """

    def method(self, left, right):
        return BinOp(left, right, op)

    return method


@v_args(inline=True)
class LoxTransformer(Transformer):
    # Programa
    def program(self, *stmts):
        return Program(list(stmts))

    # Operações matemáticas básicas
    mul = op_handler(op.mul)
    div = op_handler(op.truediv)
    sub = op_handler(op.sub)
    add = op_handler(op.add)

    # Comparações
    gt = op_handler(op.gt)
    lt = op_handler(op.lt)
    ge = op_handler(op.ge)
    le = op_handler(op.le)
    eq = op_handler(op.eq)
    ne = op_handler(op.ne)

    def VAR(self, token):
        name = str(token)
        return Var(name)

    def NUMBER(self, token):
        num = float(token)
        return Literal(num)
