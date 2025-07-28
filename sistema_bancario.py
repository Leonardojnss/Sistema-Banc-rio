import datetime
import textwrap
def principal():
    LIMITE_SAQUE = 3
    agencia = "00001"
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    usuarios = []
    contas = []
    while True:
        opcao = menu()
        if opcao == "1":
            valor = float(input("informe o valor do deposito: "))
            saldo, extrato = depositar(saldo, valor, extrato)
        elif opcao == "2":
            valor = float(input("informe o valor do saque: "))
            saldo, extrato, numero_saques = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUE,
            )
        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)
        elif opcao == "4":
            criar_usuario(usuarios)
        elif opcao == "5":
            numero_conta = len(contas) +1
            conta = criar_conta(agencia, numero_conta , usuarios)
            if conta :
                contas.append(conta)
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

def depositar(saldo, valor, extrato, /):
    if valor > 0 :
        saldo = saldo + valor
        extrato += f"deposito:\tR$ {valor:.2f}\n"
        print("\ndeposito realizado com sucesso!")
    else:
        print("\n operação falhou, o valor informado é invalido.")
    return saldo, extrato

def sacar(*,saldo,valor,extrato,limite,numero_saques,limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques
    if excedeu_saldo:
        print("\n operação falhou, voce não tem saldo sufucuente.")
    elif excedeu_limite :
        print("\n operação falhou! o valor do saque excede o limite")
    elif excedeu_saques:
        print("\n operação falhou, numeor maximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"\nsaque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print("\n saque realizado com sucesso!")
    else:
        print("\n operação falhou, o valor informado é invalido.")
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, /,*,extrato):
    print("\n===========extrto===========")
    print("não foram realizados movimentações." if not extrato else extrato)
    print(f"\nsaldo:\t\tR$ {saldo:.2f}")
    print("============================")

def criar_usuario(usuarios):
    cpf = input("informe o cpf: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario :
        print("\n já existe usuario com esse cpf.")
        return
    nome = input("informe o seu nome: ")
    data_nascimento = input("informe a data de nascimento (dd-mm-aaaa)")
    endereco = input("infome seu endedreço(logradouro, nro-bairro-cidade-/sigla estado)")
    usuarios.append({"nome":nome,"data_nascimento":data_nascimento,"cpf":cpf,"endereco":endereco})
    print("usuario criado com suceeso!")

def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf ]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("informe o cpf do usuario: ")
    usuario = filtrar_usuario(cpf, usuarios)
    if usuario:
        print("\n conta criada com sucesso.")
        return{"agencia":agencia,"numero_conta":numero_conta,"usuario":usuario}
    print("\n usuario não encontrado, fluxo de criação de conta encerrado!")

def listar_contas(contas):
    for conta in contas:
        linha = f"""\
            agencia:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100)
        print(textwrap.dedent(linha))

principal()