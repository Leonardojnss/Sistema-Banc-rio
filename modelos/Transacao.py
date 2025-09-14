from abc import ABC, abstractmethod
from datetime import datetime

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor