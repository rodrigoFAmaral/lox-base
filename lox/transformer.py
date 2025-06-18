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
    #Programa 

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

    # Outras expressões

    def call(self, callee, arguments):
        return Call(callee, arguments)

    # Parâmetros
    def params(self, *args):
        return list(args)

    # Acesso a atributo    
    def getattr(self, obj_expr, attr_name):
        return Getattr(obj_expr, str(attr_name))
    

    # Comandos e literais
    def block(self, *stmts):
        return Block(list(stmts))
    
    def assign(self, var_token, value_expr):
        if isinstance(var_token, Var):
            name = var_token.name
        else:
            name = str(var_token)
        return Assign(name, value_expr)
    
    def print_cmd(self, expr):
        return Print(expr)
    
    def if_cmd(self, cond: Expr, then: Stmt, orelse: Stmt = Block([])):
        return If(cond, then, orelse)

    def while_cmd(self, cond: Expr, body: Stmt):
        return While(cond, body)

    def for_cmd(self, for_args: tuple, body: Stmt):
        """
        Fazemos a transformação (desugar)

        De:
            for (init; cond; incr) body

        Para:
        {
            init
            while (cond) {
                body;
                incr;
            }
        }
        """
        init, cond, incr = for_args
        return Block(
            [
                init,
                While(
                    cond,
                    Block(
                        [
                            body,
                            incr,
                        ]
                    ),
                ),
            ]
        )

    def for_args(self, arg1, arg2, arg3):
        return (arg1, arg2, arg3)

    def opt_expr(self, arg=None):
        if arg is None:
            arg = True
        return arg
    
    def fun_def(self, name: Var, args: list[str], body: Block):
        return Function(name.name, args, body.stmts)
        
    def fun_args(self, *args: Var) -> list[str]:
        return [arg.name for arg in args]
    
    def return_cmd(self, expr: Expr = Literal(None)):
        return Return(expr)

    def VAR(self, token):
        return Var(str(token))

    def NUMBER(self, token):
        return Literal(float(token))
    
    def STRING(self, token):
        return Literal(str(token)[1:-1])
    
    def NIL(self, _):
        return Literal(None)

    def BOOL(self, token):
        return Literal(token == "true")

    def logand(self, left, _and, right):
        return And(left, right)

    def logor(self, left, _or, right):
        return Or(left, right)

    def setattr(self, obj, attr_name, value_expr):
        return Setattr(obj, str(attr_name), value_expr)

    def neg(self, expr):
        return UnaryOp(expr, op.neg)

    def not_(self, expr):
        return UnaryOp(expr, op.not_)