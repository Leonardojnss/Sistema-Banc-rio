saldo = 1000.00
limite_de_saque_diario = 3
numero_de_saques_hoje = 0
historico_de_saques = []
historico_de_deposito = []
while True:
    operacao = int(input("Informe qual a operação que deseja realizar.\nDigite\n[1] Sacar\n[2] depositar\n[3] Ver Extrato\n[4] Sair\n: "))
    print()
    if operacao == 1:
        while True:
            if numero_de_saques_hoje == limite_de_saque_diario:
                print(f"Voçê já atingiu o seu limite de saque diário que é de {limite_de_saque_diario } por dia.\nEspere até o outro dia para poder sacar.")
                break
            sacar = float(input(f"O seu saldo da conta é de {saldo:.2f} reais.\nVoçê tem {limite_de_saque_diario - numero_de_saques_hoje} saques restantes.\nO limite de saque individual é de 500 reais.\nQuanto o Senhor(a) deseja sacar: "))
            print()
            if sacar <= 0:
                print("O valor do saque deve ser positivo!!\nTente novamente.")
            elif sacar > 500:
                print(f"o senhor não tem o limite diário de {sacar:.2f}, o seu limite por saque é de 500 reais.\nTente novamente sacar com outo valor.")
                print()
            elif sacar > saldo:
                print(f"ERRO!\nSaldo insuficiente.\nSeu saldo atual é de {saldo:.2f} reais.\nTente novamente.")
                print()
            else:
                numero_de_saques_hoje = numero_de_saques_hoje + 1
                saldo -= sacar
                historico_de_saques.append(sacar)
                print(f"Saque realizado com sucesso no valor de {sacar:.2f} reais!\nNovo saldo de {saldo:.2f} reais.\n")
                print(f"Novo saldo de {saldo:.2f} reais.")
                print("Após essa operação o senhor(a) voltará para o início.")
                print()
                break
    elif operacao == 2:
        depositar = float(input("Quanto o senhor(a) deseja depositar: "))
        if depositar > 0:
            saldo += depositar
            historico_de_deposito.append(depositar)
            print(f"O deposito de {depositar:.2f} reais foi depositado na sua conta.\nO seu saldo atual é de {saldo:.2f} reais.")
            print("Obrigado pela preferencia, o senhor(a) será direcionado para o início.")
        else:
            print("Valor de depósito inválido!!")
        print()
    elif operacao == 3:
        print(f"-----EXTRATO-----\nO seu saldo é de {saldo:.2f} reais")
        if historico_de_saques:
            print("\n-----HITÓRIO DE SAQUES-----")
            for saque in historico_de_saques:
                print(f"saque de: {saque:.2f} reais.")
        else:
            print("nenhum saque registrado")
        if historico_de_deposito:
            print(f"\n-----HISTÓRICO DE DEPÓSITO-----")
            for deposito in historico_de_deposito:
                print(f"depósito de: {deposito:.2f} reais.")
        else:
            print("nenhum depósito registrado")
        print()
    elif operacao == 4:
        print("Saindo do sistema.")
        break
    else:
        print("Operação invalida!")
        print()