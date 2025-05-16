import builtins
import math
from types import SimpleNamespace

import pytest
from lark import Tree

from lox import *
from lox.ast import *
from lox.testing import ExampleTester


@pytest.fixture
def expr():
    return True


@pytest.fixture
def src():
    return "sqrt(2 + 2)"


@pytest.fixture
def src_():
    return "obj.method(1, 2, 3)"


@pytest.fixture
def src__():
    return 'foo("arg")("sub-arg-1", sub_arg_2())'


def test_suporta_chamada_de_função_na_cst(cst: Tree):
    assert "sqrt" in cst.pretty()
    assert "2" in cst.pretty()


def test_suporta_chamada_de_método_na_cst(cst_: Tree):
    assert "obj" in cst_.pretty()
    assert "method" in cst_.pretty()
    assert "1" in cst_.pretty()
    assert "2" in cst_.pretty()
    assert "3" in cst_.pretty()


def test_suporta_chamada_de_funções_aninhadas_na_cst(cst_: Tree):
    assert "foo" in cst_.pretty()
    assert "sub_arg_2" in cst_.pretty()
    assert "arg" in cst_.pretty()
    assert "sub-arg-1" in cst_.pretty()


def test_suporta_chamada_de_função_na_ast(ast, ast_, ast__):
    assert isinstance(
        ast, Call
    ), "esperava encontrar um nó Call para representar chamadas de funções"
    assert isinstance(
        ast_, Call
    ), "não é necessário criar um nó específico para methodos"
    assert isinstance(
        ast__, Call
    ), "reaproveite o nó Call para suportar chamadas de funções aninhadas"


def test_renomeou_o_atributo_name_da_ast(ast: Call):
    if hasattr(ast, "name"):
        msg = "Renomeie o atributo Call.name já que agora devemos guardar um nó e não uma string."
        raise ValueError(msg)


def test_implementa_a_função_eval(exs):
    def ctx():
        return {
            "sqrt": math.sqrt,
            "obj": SimpleNamespace(method=lambda *args: args),
            "foo": lambda *args: lambda *args2: args + args2,
        }

    for ex in exs:
        print(f"Testando {ex.src=}")
        expect = builtins.eval(ex.src, ctx())
        result = ex.ast.eval(ctx())

        assert (
            result == expect
        ), f"[Call.eval]: esperava {expect} mas encontrei {result}"


class TestExamples(ExampleTester):
    module = "call"
    examples = {"bool", "nil", "num", "string"}
