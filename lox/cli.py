"""
Esse módulo usa a biblioteca `argparse` para criar uma interface de linha de comando
(CLI) para o compilador de Lox.

Ele permite que o usuário execute o compilador com diferentes opções, como especificar
o arquivo de entrada, ativar o modo para imprimir as árvores
sintáticas, lexer, etc.

Argparse talvez não seja a melhor opção para criar uma CLI, mas é uma biblioteca
padrão do Python e não requer instalação de dependências externas.
"""

import argparse

from lark import ParseError
from .ast import Var
from .ctx import Ctx
from .lox import parse, parse_cst, lex
from .runtime import lox_show


def make_argparser():
    parser = argparse.ArgumentParser(description="Compilador Lox")
    parser.add_argument(
        "file",
        help="Arquivo de entrada",
    )
    parser.add_argument(
        "-t",
        "--ast",
        action="store_true",
        help="Imprime a árvore sintática.",
    )
    parser.add_argument(
        "-l",
        "--lex",
        action="store_true",
        help="Imprime o lexer.",
    )
    parser.add_argument(
        "-c",
        "--cst",
        action="store_true",
        help="Imprime a árvore sintática concreta produzida pelo Lark.",
    )
    return parser


def main():
    """
    Função principal que cria a interface de linha de comando (CLI) para o compilador Lox.
    """
    parser = make_argparser()
    args = parser.parse_args()

    # Lê arquivo de entrada
    try:
        with open(args.file, "r") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Arquivo {args.file} não encontrado.")
        exit(1)

    if args.file.endswith(".elox"):
        ctx = Ctx()
        for line in source.splitlines():
            line = line.strip()
            if line.startswith("//") or not line:
                continue
            process_source_line(line, args, ctx=ctx)

    elif not args.ast and not args.cst and not args.lex:
        run(source)
    else:
        debug_source(source, args)


def debug_source(source: str, args, expr: bool = False):
    """
    Mostra informações de depuração sobre o código Lox passado como argumento.
    """
    if args.ast:
        ast = parse(source, expr=expr)
        print(ast.pretty())

    if args.cst:
        cst = parse_cst(source, expr=expr)
        print(cst.pretty())

    if args.lex:
        for token in lex(source):
            print(f"{token.type}: {token.value}")


def process_source_line(source: str, args, ctx: Ctx):
    """
    Processa uma linha de código Lox e executa o commando correspondente.
    """

    try:
        from rich import print

        print(f"[red bold]{source}")
    except ImportError:
        print(source)

    if not args.ast and not args.cst and not args.lex:
        run_expr(source, ctx)
    else:
        debug_source(source, args, expr=True)


def run(source: str):
    """
    Executa o código Lox passado como argumento.

    Essa função é chamada quando o usuário não especifica nenhuma opção de
    impressão. Ela executa o código Lox normalmente.
    """
    module = parse(source)
    module["main"].eval(Ctx())


def run_expr(source: str, ctx: Ctx):
    """
    Executa a expressão Lox passada como argumento.

    Pergunta para o usuário o valor de todas as variáveis usadas na expressão.
    """

    ast = parse(source, expr=True)

    def ask_var(var: Var):
        print(ctx)
        if var.name in ctx:
            return

        value = input(f"  {var.name}: ")
        if value in ("", "nil"):
            ctx[var.name] = None
            return

        try:
            expr_ast = parse(value, expr=True)
        except ParseError:
            print(f"Erro ao avaliar expressão: {value}")
            ask_var(var)
        else:
            ctx[var.name] = expr_ast.eval(ctx)

    ast.visit({Var: ask_var})
    value = ast.eval(ctx)
    print(f"-> {lox_show(value)}")
