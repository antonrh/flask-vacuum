from injector import Module, inject, provider

from flask_vacuum import contracts


class Scanner(contracts.Scanner):
    def scan(self) -> None:
        pass


class ScannerModule(Module):
    @inject
    @provider
    def provide_scanner(self) -> contracts.Scanner:
        return Scanner()
