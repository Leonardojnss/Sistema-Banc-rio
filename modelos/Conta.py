from modelos.Cliente import Pessoa_fisica
from modelos.Transacao import Saque
from datetime import datetime

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0 
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls,cliente,numero):
        return cls(numero,cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico

class Conta_corrente(Conta):
    def __init__(self, numero, cliente,limite=500,limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def __str__(self):
        return f"""\
            Agnência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property
    def transacoes(self):
        return self._transacoes