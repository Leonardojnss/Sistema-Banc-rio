class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

class Pessoa_fisica(Cliente):
    def __init__(self,nome, data_nascimento,cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf