from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class Pessoa_fisica(Cliente):
    def __init__(self,nome, data_nascimento,cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

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
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor >saldo

        if excedeu_saldo:
            print("Operação falhou ! Você não tem saldo suficiente !")

        elif valor > 0:
            self._saldo -= valor
            print("Saque realizado com sucesso")
            return True
        
        else:
            print("Operação falhou ! O valor informado é inválido.")
        return False
        
    def depositar(self,valor):
        if valor > 0 :
            self._saldo += valor
            print("Depósito realizado com sucesso !")

        else:
            print("Operação falhou ! O valor informado é invalido") 
            return False
        
        return True

class Conta_corrente(Conta):
    def __init__(self, numero, cliente,limite=500,limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__ ]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite :
            print("Operação falhou! O valor do saque excede o limite.")
        
        elif excedeu_saques:
            print("Operação falhou! O numero máximo de saques excedido. ")
        
        else:
            return super().sacar(valor)
        
        return False
    
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
    
    def adicionar_transacao(self,transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime
                ("%d-%m-%Y %H:%M:%S"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self,valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def principal():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "1":
            depositar(clientes)

        elif opcao == "2":
            sacar(clientes)

        elif opcao == "3":
            exibir_extrato(clientes)

        elif opcao == "4":
            criar_cliente(clientes)

        elif opcao == "5":
            numero_conta = len(contas) +1
            criar_conta(numero_conta, clientes , contas)

        elif opcao == "6":
            listar_contas(contas)

        elif opcao == "7":
            break
        else:
            print("Operação invalida, tente novamente!")

def menu():

    menu = """\n
    ====================menu==================
    [1]DEPOSITAR
    [2]SACAR
    [3]EXTRATO
    [4]NOVO USUÁRIO
    [5]NOVA CONTA
    [6]LISTAR CONTAS
    [7]SAIR
    """
    return input(textwrap.dedent(menu))

def depositar(clientes):
    cpf = input("informe o seu cpf: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("cliente não encontrado!")
        return
    
    valor = float(input("informe o valor do depósito: "))

    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta,transacao)

def sacar(clientes):
    cpf = input("informe o seu cpf: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("cliente não encontrado!")
        return
    
    valor = float(input("informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta,transacao)

def exibir_extrato(clientes):
    cpf = input("informe o seu cpf: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("cliente não encontrado!")
        return
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n==========EXTRATO==========")
    transacoes = conta.historico.transacoes

    # retirei o // extrato = ""
    if not transacoes:
        print("não foram realizadas movimentações")

    else:
        for transacao in transacoes:
            print (f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}")

    #  print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("===========================")

def criar_cliente(clientes):
    cpf = input("informe o cpf: ")
    usuario = filtrar_cliente(cpf, clientes)

    if usuario :
        print("\n já existe usuario com esse cpf.")
        return
    
    nome = input("informe o seu nome: ")
    data_nascimento = input("informe a data de nascimento (dd-mm-aaaa)")
    endereco = input("infome seu endedreço(logradouro, nro-bairro-cidade-/sigla estado)")

    cliente = Pessoa_fisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)

    print("Cliente criado com suceeso!")

def criar_conta( numero_conta,clientes, contas):
    cpf = input("informe o cpf do usuario: ")
    cliente = filtrar_cliente(cpf, clientes)
    if not cliente:
        print("cliente não encontrado, fluxo de criação de conta encerrado")
        return
    
    conta = Conta_corrente.nova_conta(cliente=cliente,numero=numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)      # ficar de olho troquei o  // cliente.contas.append() 

    print("\nconta criada com sucesso")

def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf ]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("cliente não possui conta!")
        return
    
    # FIXME: nõa permite cliente escolher a conta
    return cliente.contas[0]

principal()