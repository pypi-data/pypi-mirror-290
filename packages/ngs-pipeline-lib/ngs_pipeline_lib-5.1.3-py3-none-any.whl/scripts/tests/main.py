import importlib

from clidantic import Parser  # type: ignore

cli = Parser()


def test():
    importlib.import_module("scripts.tests.e2e")
    importlib.import_module("scripts.tests.integration")
    cli()
