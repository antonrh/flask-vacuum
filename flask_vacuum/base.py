from typing import List, Optional

from flask import Flask
from flask_injector import FlaskInjector, _ModuleT as ModuleT  # noqa

from flask_vacuum.events import EventsModule
from flask_vacuum.scanner import ScannerModule


class Vacuum:

    default_modules: List[ModuleT] = [ScannerModule, EventsModule]

    def __init__(
        self,
        app: Optional[Flask] = None,
        modules: Optional[List[ModuleT]] = None,
        add_default_modules: bool = True,
    ):
        if app:
            self.init_app(app, modules=modules, add_default_modules=add_default_modules)

    def init_app(
        self,
        app: Flask,
        modules: Optional[List[ModuleT]] = None,
        add_default_modules: bool = True,
    ):
        if modules is None:
            modules = []

        if add_default_modules:
            for index, module in enumerate(self.default_modules):
                modules.insert(index, module)

        FlaskInjector(app, modules=modules)


def init_app(
    app: Flask,
    modules: Optional[List[ModuleT]] = None,
    add_default_modules: bool = True,
):
    vacuum = Vacuum()
    vacuum.init_app(app, modules=modules, add_default_modules=add_default_modules)
