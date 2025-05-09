import re
import pytest


MY_NUMBER_RE = re.compile(r"([1-9][0-9]*|0)(\.[0-9]+)?")
LOX_NUMBER_RE = re.compile(r"[0-9]+(\.[0-9]+)?")


@pytest.fixture
def mod(mod_loader):
    """
    Fixture para o módulo que contém as expressões regulares.
    """
    return mod_loader("lex_numeros")


def test_valid_in_both(mod):
    valid = set(mod.VALIDOS_EM_AMBAS_ESPECIFICACOES)
    if ... in valid:
        pytest.fail("Remova o '...' da lista de exemplos")

    msg = "Você precisa adicionar cinco exemplos de números válidos em ambas as especificações"
    assert len(valid) >= 5, msg
    for num in valid:
        msg = f"{num} não é reconhecido como número válido na nossa versão"
        assert MY_NUMBER_RE.fullmatch(num), msg

        msg = f"{num} não é reconhecido como número válido na versão do Lox"
        assert LOX_NUMBER_RE.fullmatch(num), msg


def test_valid_in_lox_only(mod):
    valid = set(mod.VALIDOS_EM_LOX_E_INVALIDOS_NA_NOSSA_VERSAO)
    if ... in valid:
        pytest.fail("Remova o '...' da lista de exemplos")

    msg = "Você precisa adicionar cinco exemplos de números válidos somente em Lox"
    assert len(valid) >= 5, msg

    for num in valid:
        msg = f"{num} é reconhecido como número válido na nossa versão!"
        assert not MY_NUMBER_RE.fullmatch(num), msg

        msg = f"{num} não é reconhecido como número válido na versão do Lox"
        assert LOX_NUMBER_RE.fullmatch(num), msg


def test_valid_in_ours_only(mod):
    valid = set(mod.VALIDOS_NA_NOSSA_VERSAO_E_INVALIDOS_EM_LOX)
    if ... in valid:
        pytest.fail("Remova o '...' da lista de exemplos")

    assert len(valid) == 0, "Nossa versão somente aceita números Lox válidos."
