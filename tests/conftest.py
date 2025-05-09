from types import SimpleNamespace
import pytest
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
EXERCISES = BASE_DIR / "exercícios"


@pytest.fixture
def exercises_folder():
    """
    Retorna o caminho para a pasta de exercícios.
    """
    return EXERCISES


@pytest.fixture
def mod_loader(exercises_folder: Path):
    """
    Retorna o caminho para a pasta de exercícios.
    """

    def loader(name: str):
        file = exercises_folder / f"{name}.py"
        if not file.exists():
            raise FileNotFoundError(f"Arquivo {file} não encontrado.")

        ns = {}
        with file.open("r") as fd:
            exec(fd.read(), ns)

        return SimpleNamespace(**ns)

    return loader
