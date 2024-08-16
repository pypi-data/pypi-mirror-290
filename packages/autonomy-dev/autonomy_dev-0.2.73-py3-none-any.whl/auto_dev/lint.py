"""Simple linting tooling for autonomy repos."""

from auto_dev.utils import isolated_filesystem

from .cli_executor import CommandExecutor


def check_path(path: str, verbose: bool = False) -> bool:
    """Check the path for linting errors.
    :param path: The path to check.
    """
    with isolated_filesystem(True):
        command = CommandExecutor(["poetry", "run", "ruff", "check", "--fix", "--unsafe-fixes", path])
        return command.execute(verbose=verbose)
