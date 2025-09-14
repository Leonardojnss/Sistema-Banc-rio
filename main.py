import textwrap
from database import conectar
import mysql.connector
from decimal import Decimal

def principal():

    while True:
        opcao = menu()

        if opcao == "1":
            depositar()

        elif opcao == "2":
            sacar()

        elif opcao == "3":
            exibir_extrato()

        elif opcao == "4":
            criar_cliente()

        elif opcao == "5":
            conexao = conectar()
            if conexao:
                cursor = conexao.cursor()
                cursor.execute("SELECT MAX(numero) FROM contas")
                resultado = cursor.fetchone()
                ultimo_numero = resultado[0] if resultado[0] is not None else 0
                numero_conta = ultimo_numero + 1
                criar_conta(numero_conta)
                conexao.close()
            else:
                print("\nFalha ao conectar ao banco para obter número da conta.")

        elif opcao == "6":
            listar_contas()

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

def depositar():
    conexao = None
    
    try:
        # Obter os dados do usuário
        numero_conta = int(input("Informe o número da conta para depósito: "))
        valor = Decimal(input("Informe o valor do depósito: "))

        if valor <= 0:
            print("\nValor de depósito inválido.")
            return

        # Conectar ao banco
        conexao = conectar()
        if not conexao:
            print("\nFalha na conexão com o banco de dados.")
            return
        
        cursor = conexao.cursor()

        # Buscar a conta e seu saldo atual
        # Lembrar que o nome da coluna é 'idContas'
        query_busca_conta = "SELECT idContas, saldo FROM contas WHERE numero = %s"
        cursor.execute(query_busca_conta, (numero_conta,))
        resultado_conta = cursor.fetchone()

        if not resultado_conta:
            print("\nConta não encontrada.")
            return
        
        conta_id, saldo_atual = resultado_conta

        # Atualizar o saldo na tabela 'contas'
        novo_saldo = saldo_atual + valor
        query_update_saldo = "UPDATE contas SET saldo = %s WHERE idContas = %s"
        cursor.execute(query_update_saldo, (novo_saldo, conta_id))

        # Inserir o registro na tabela 'transacoes'
        # Lembrar que a coluna de chave estrangeira é 'Contas_idContas'
        from datetime import datetime
        data_transacao = datetime.now()
        
        query_insert_transacao = """
        INSERT INTO transacoes (tipo, valor, data, Contas_idContas)
        VALUES (%s, %s, %s, %s)
        """
        dados_transacao = ("Deposito", valor, data_transacao, conta_id)
        cursor.execute(query_insert_transacao, dados_transacao)

        #Efetivar a transação (salvar as duas alterações)
        conexao.commit()
        print("\nDepósito realizado com sucesso!")

    except mysql.connector.Error as err:
        print(f"\nOcorreu um erro durante o depósito: {err}")
        if conexao:
            conexao.rollback() # Desfaz as alterações em caso de erro

    finally:
        # Fechar a conexão
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

def sacar():
    conexao = None
    try:
        #Para obter os dados do usuário
        numero_conta = int(input("Informe o número da conta para o saque: "))
        valor = Decimal(input("Informe o valor do saque: "))

        #Conectar ao banco
        conexao = conectar()
        if not conexao:
            print("\nFalha na conexão com o banco de dados.")
            return
        
        cursor = conexao.cursor(dictionary=True) # Usar dictionary=True facilita o acesso às colunas

        # Buscar os dados da conta para verificação
        query_busca_conta = "SELECT idContas, saldo, limite, limite_saques FROM contas WHERE numero = %s"
        cursor.execute(query_busca_conta, (numero_conta,))
        conta = cursor.fetchone()

        if not conta:
            print("\nConta não encontrada.")
            return

        # Buscar o número de saques já realizados
        query_conta_saques = "SELECT COUNT(*) AS total_saques FROM transacoes WHERE Contas_idContas = %s AND tipo = 'Saque'"
        cursor.execute(query_conta_saques, (conta['idContas'],))
        resultado_saques = cursor.fetchone()
        numero_saques = resultado_saques['total_saques']
        
        # Aplicar as regras de negócio
        excedeu_saldo = valor > conta['saldo']
        excedeu_limite = valor > conta['limite']
        excedeu_saques = numero_saques >= conta['limite_saques']

        if excedeu_saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")
        elif excedeu_limite:
            print("\nOperação falhou! O valor do saque excede o limite da conta.")
        elif excedeu_saques:
            print("\nOperação falhou! Número máximo de saques excedido.")
        elif valor > 0:
            # Se todas as regras passaram, efetuar o saque
            novo_saldo = conta['saldo'] - valor
            query_update_saldo = "UPDATE contas SET saldo = %s WHERE idContas = %s"
            cursor.execute(query_update_saldo, (novo_saldo, conta['idContas']))

            from datetime import datetime
            data_transacao = datetime.now()
            
            query_insert_transacao = """
            INSERT INTO transacoes (tipo, valor, data, Contas_idContas)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query_insert_transacao, ("Saque", valor, data_transacao, conta['idContas']))

            conexao.commit()
            print("\nSaque realizado com sucesso!")
        else:
            print("\nOperação falhou! O valor informado é inválido.")

    except mysql.connector.Error as err:
        print(f"\nOcorreu um erro durante o saque: {err}")
        if conexao:
            conexao.rollback()

    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

def exibir_extrato():
    conexao = None

    try:
        #Obter número da conta e conectar ao banco
        numero_conta = int(input("Informe o número da conta para exibir o extrato: "))
        conexao = conectar()
        if not conexao:
            print("\nFalha na conexão com o banco de dados.")
            return
        
        # Usar dictionary=True para facilitar o acesso aos dados
        cursor = conexao.cursor(dictionary=True)

        #  Buscar os dados principais da conta (ID e Saldo)
        query_busca_conta = "SELECT idContas, saldo FROM contas WHERE numero = %s"
        cursor.execute(query_busca_conta, (numero_conta,))
        conta = cursor.fetchone()

        if not conta:
            print("\nConta não encontrada.")
            return
        
        # Com o ID da conta, buscar todas as transações no histórico
        conta_id = conta['idContas']
        query_transacoes = "SELECT tipo, valor, data FROM transacoes WHERE Contas_idContas = %s ORDER BY data"
        cursor.execute(query_transacoes, (conta_id,))
        transacoes = cursor.fetchall() # fetchall() pega TODAS as linhas do resultado

        # Exibir o extrato formatado
        print("\n================== EXTRATO ==================")
        if not transacoes:
            print("Não foram realizadas movimentações.")
        else:
            for transacao in transacoes:
                # Formatando a data para ficar mais legível
                data_formatada = transacao['data'].strftime('%d/%m/%Y %H:%M:%S')
                valor_formatado = f"R$ {transacao['valor']:.2f}"
                print(f"{data_formatada} - {transacao['tipo']:<10} | {valor_formatado}")
        
        print("-" * 45)
        print(f"Saldo Atual: R$ {conta['saldo']:.2f}")
        print("============================================")

    except mysql.connector.Error as err:
        print(f"\nOcorreu um erro ao exibir o extrato: {err}")

    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

def criar_cliente():
    cpf = input("informe o cpf: ")
    conexao = conectar()

    if not conexao :
        print("\nNão foi possível conectar ao banco de dados .")
        return
    
    cursor = conexao.cursor()

    # 1. Verificar se o cliente já existe
    query_verificacao = "SELECT cpf FROM clientes WHERE cpf = %s"
    cursor.execute(query_verificacao, (cpf,))
    usuario_existente = cursor.fetchone()

    if usuario_existente:
        print("\nJá existe um usuário com este CPF.")
        cursor.close()
        conexao.close()
        return
    
    # 2. Se não existe, pedir os dados e inserir
    nome = input("informe o seu nome: ")
    data_nascimento = input("informe a data de nascimento (dd-mm-aaaa)")
    endereco = input("infome seu endedreço(logradouro, nro-bairro-cidade-/sigla estado)")

    query_insercao = "INSERT INTO clientes (nome, data_nascimento, cpf, endereco) VALUES (%s, %s, %s, %s)"
    dados_cliente = (nome, data_nascimento, cpf, endereco)

    try:
        cursor.execute(query_insercao, dados_cliente)
        conexao.commit() # Confirma e salva a inserção no banco
        print("\nCliente criado com sucesso!")
    except mysql.connector.Error as err:
        print(f"\nFalha ao inserir cliente: {err}")
        conexao.rollback() # Desfaz a operação em caso de erro
    finally:
        # 3. Fechar o cursor e a conexão
        cursor.close()
        conexao.close()

def criar_conta( numero_conta):
    cpf = input("informe o cpf do usuario: ")
    conexao = conectar()
    if not conexao:
        print("cliente não encontrado, fluxo de criação de conta encerrado")
        return
    
    cursor = conexao.cursor()

    try:
        # 2. Buscar o ID do cliente na tabela 'clientes' usando o CPF
        #    Precisamos do ID para usar como chave estrangeira na tabela 'contas'
        query_busca_cliente = "SELECT idClientes FROM clientes WHERE cpf = %s"
        cursor.execute(query_busca_cliente, (cpf,))
        resultado = cursor.fetchone() # Pega o primeiro resultado encontrado

        # Verificar se o cliente foi encontrado
        if not resultado:
            print("\nCliente não encontrado com o CPF informado. Operação cancelada.")
            return

        cliente_id = resultado[0] 

        # 4. Definir os dados da nova conta e inserir na tabela 'contas'
        agencia = "0001"
        saldo_inicial = 0
        limite = 500
        limite_saques = 3
        
        query_insercao_conta = """
        INSERT INTO contas (agencia, numero, saldo, limite, limite_saques, Clientes_idClientes)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        dados_nova_conta = (agencia, numero_conta, saldo_inicial, limite, limite_saques, cliente_id)

        cursor.execute(query_insercao_conta, dados_nova_conta)
        conexao.commit() # Salva a nova conta no banco

        print("\nConta criada com sucesso!")

    except mysql.connector.Error as err:
        print(f"\nOcorreu um erro ao criar a conta: {err}")
        conexao.rollback()
    
    finally:
        # 5. Fechar a conexão
        cursor.close()
        conexao.close()     

def listar_contas(contas):
    conexao = None
    try:
        conexao = conectar()
        if not conexao:
            print("\nFalha na conexão com o banco de dados.")
            return
        
        cursor = conexao.cursor(dictionary=True)

        # O Comando SQL com JOIN
        # Este comando busca dados de duas tabelas ao mesmo tempo.
        query = """
        SELECT
            c.agencia,
            c.numero,
            c.saldo,
            cl.nome AS nome_titular
        FROM
            contas AS c
        JOIN
            clientes AS cl ON c.Clientes_idClientes = cl.idClientes
        ORDER BY
            c.numero;
        """
        
        cursor.execute(query)
        contas = cursor.fetchall()

        # Exibir a lista de contas
        print("\n================== LISTA DE CONTAS ==================")
        if not contas:
            print("Nenhuma conta cadastrada.")
        else:
            for conta in contas:
                print(f"""
---------------------------------------------------
Titular:  {conta['nome_titular']}
Agência:  {conta['agencia']}
Conta Nº: {conta['numero']}
Saldo:    R$ {conta['saldo']:.2f}
                """)
        print("===================================================")

    except mysql.connector.Error as err:
        print(f"\nOcorreu um erro ao listar as contas: {err}")

    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

principal()