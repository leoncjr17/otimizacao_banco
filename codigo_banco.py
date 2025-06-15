class FuncoesBancarias:
    LIMITE_SAQUES = 3

    def __init__(self):
        pass

    def saque(self, conta, valor):
        if valor <= 0:
            print("Valor do saque deve ser positivo.")
            return False

        if conta["nro_saques"] < FuncoesBancarias.LIMITE_SAQUES:
            if valor <= conta["saldo"]:
                conta["saldo"] -= valor
                conta["nro_saques"] += 1
                conta["extrato"].append(("Saque", valor))
                print(f"Saque de R${valor:.2f} realizado com sucesso.")
                return True
            else:
                print("Saldo insuficiente para o saque.")
        else:
            print("Limite de saques diários atingido.")
        return False

    def deposito(self, conta, valor):
        if valor <= 0:
            print("Valor do depósito deve ser positivo.")
            return False
        
        conta["saldo"] += valor
        conta["extrato"].append(("Depósito", valor))
        print(f"Depósito de R${valor:.2f} realizado com sucesso.")
        return True
    
    def exibir_extrato(self, conta):
        print(f"\n=== EXTRATO CONTA {conta['agencia']}-{conta['numero_conta']} ===")
        print(f"Titular: {conta['usuario']['nome']}")
        print(f"CPF: {conta['usuario']['cpf']}") # Exibe o CPF canônico armazenado
        print(f"Saldo atual: R$ {conta['saldo']:.2f}")
        
        if not conta["extrato"]:
            print("Não foram realizadas movimentações.")
        else:
            print("\nMovimentações:")
            for tipo_movimentacao, valor_movimentacao in conta["extrato"]:
                print(f"- {tipo_movimentacao}: R$ {valor_movimentacao:.2f}")
        print("====================")

class ContaUsuarios:
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self._numero_conta_atual = 1

    @staticmethod
    def _sanitizar_e_validar_cpf(cpf_str: str) -> str | None:
        """
        Sanitiza o CPF para conter apenas dígitos e valida se tem 11 dígitos.
        Retorna o CPF sanitizado de 11 dígitos ou None se inválido.
        """
        if not isinstance(cpf_str, str):
            return None 
        
        cpf_sanitizado = "".join(filter(str.isdigit, cpf_str))
        
        if len(cpf_sanitizado) == 11:
            return cpf_sanitizado
        else:
            
            return None

    def criar_usuario(self, nome, data_nascimento, cpf_raw, endereco):
        cpf_canonico = ContaUsuarios._sanitizar_e_validar_cpf(cpf_raw)

        if not cpf_canonico:
            print(f"Erro: CPF '{cpf_raw}' fornecido é inválido. Deve conter 11 dígitos numéricos (após remover formatação).")
            return

        if self._buscar_usuario_por_cpf(cpf_raw): 
            print(f"Erro: Usuário com CPF que resulta em '{cpf_canonico}' já cadastrado!")
            return

        usuario = {
            "nome": nome,
            "data_nascimento": data_nascimento,
            "cpf": cpf_canonico,  
            "endereco": endereco
        }
        self.usuarios.append(usuario)
        print(f"Usuário {nome} cadastrado com sucesso!")

    def _buscar_usuario_por_cpf(self, cpf_raw: str):
        """
        Busca um usuário pelo CPF. O CPF de entrada é sanitizado e validado.
        Retorna o dicionário do usuário se encontrado, caso contrário None.
        """
        cpf_canonico_para_busca = ContaUsuarios._sanitizar_e_validar_cpf(cpf_raw)

        if not cpf_canonico_para_busca:

            return None 

        for usuario_armazenado in self.usuarios:

            if usuario_armazenado["cpf"] == cpf_canonico_para_busca:
                return usuario_armazenado
        return None

    def criar_conta(self, cpf_usuario_raw):
        usuario_encontrado = self._buscar_usuario_por_cpf(cpf_usuario_raw)

        if usuario_encontrado is None:
            print(f"Erro: Usuário com CPF fornecido ('{cpf_usuario_raw}') não encontrado ou CPF inválido. Não é possível criar a conta.")
            return None

        nova_conta = {
            "agencia": "0001",
            "numero_conta": self._numero_conta_atual,
            "usuario": usuario_encontrado,
            "saldo": 0.0,
            "extrato": [],
            "nro_saques": 0
        }
        self.contas.append(nova_conta)
        self._numero_conta_atual += 1
        print(f"Conta {nova_conta['numero_conta']} criada com sucesso para o usuário {usuario_encontrado['nome']}.")
        return nova_conta

    def buscar_contas_por_cpf(self, cpf_raw: str):
        usuario = self._buscar_usuario_por_cpf(cpf_raw)
        
        if not usuario:
            return [] 
        
        contas_do_usuario = [conta for conta in self.contas if conta["usuario"]["cpf"] == usuario["cpf"]]
        return contas_do_usuario