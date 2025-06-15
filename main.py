from codigo_banco import ContaUsuarios, FuncoesBancarias

def selecionar_conta(banco, cpf):
    """
    Permite ao usuário selecionar uma conta se houver múltiplas para o CPF.
    Retorna a conta selecionada (dicionário) ou None.
    """
    contas_usuario = banco.buscar_contas_por_cpf(cpf)
    
    if not contas_usuario:
        print("Nenhuma conta encontrada para este CPF.")
        return None
    
    if len(contas_usuario) == 1:
        print(f"Conta {contas_usuario[0]['numero_conta']} selecionada automaticamente para o CPF {cpf}.")
        return contas_usuario[0]
    else:
        print("\nMúltiplas contas encontradas para este CPF:")
        for i, conta_sel in enumerate(contas_usuario):
            print(f"{i + 1}. Agência: {conta_sel['agencia']} / Conta: {conta_sel['numero_conta']}")
        
        while True:
            try:
                escolha_str = input("Digite o número da conta que deseja usar (ou deixe em branco para cancelar): ")
                if not escolha_str: 
                    print("Seleção cancelada.")
                    return None
                escolha = int(escolha_str)
                if 1 <= escolha <= len(contas_usuario):
                    return contas_usuario[escolha - 1]
                else:
                    print("Escolha inválida. Tente novamente.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

def sistema_bancario():
    banco = ContaUsuarios()      
    operacoes = FuncoesBancarias() 

    while True:
        print("\n--- Bem-vindo ao Sistema Bancário ---")
        print("Escolha uma opção:")
        print("1. Criar usuário")
        print("2. Criar conta bancária")
        print("3. Fazer depósito")
        print("4. Fazer saque")
        print("5. Consultar extrato")
        print("6. Sair")

        opcao = input("Digite o número da opção desejada: ")

        if opcao == "1":
            print("\n--- Criar Novo Usuário ---")
            nome = input("Digite o nome completo: ")
            data_nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ")
            cpf = input("Digite o CPF (apenas números): ")
            endereco = input("Digite o endereço (logradouro, nro - bairro - cidade/UF): ")
            banco.criar_usuario(nome, data_nascimento, cpf, endereco)
        
        elif opcao == "2":
            print("\n--- Criar Nova Conta Bancária ---")
            cpf_usuario = input("Digite o CPF do titular da conta (apenas números): ")
            banco.criar_conta(cpf_usuario)
        
        elif opcao == "3":
            print("\n--- Realizar Depósito ---")
            cpf_usuario = input("Digite o CPF do titular da conta para depósito: ")
            conta_selecionada = selecionar_conta(banco, cpf_usuario)
            
            if conta_selecionada:
                try:
                    valor_str = input(f"Digite o valor do depósito para a conta {conta_selecionada['numero_conta']}: R$ ")
                    if not valor_str:
                        print("Valor não fornecido. Operação cancelada.")
                    else:
                        valor = float(valor_str)
                        operacoes.deposito(conta_selecionada, valor)
                except ValueError:
                    print("Erro: Valor inválido para depósito.")
            else:
                print("Operação de depósito não realizada.")
        
        elif opcao == "4":
            print("\n--- Realizar Saque ---")
            cpf_usuario = input("Digite o CPF do titular da conta para saque: ")
            conta_selecionada = selecionar_conta(banco, cpf_usuario)

            if conta_selecionada:
                try:
                    valor_str = input(f"Digite o valor do saque da conta {conta_selecionada['numero_conta']} (Saldo: R${conta_selecionada['saldo']:.2f}): R$ ")
                    if not valor_str:
                        print("Valor não fornecido. Operação cancelada.")
                    else:
                        valor = float(valor_str)
                        operacoes.saque(conta_selecionada, valor)
                except ValueError:
                    print("Erro: Valor inválido para saque.")
            else:
                print("Operação de saque não realizada.")
        
        elif opcao == "5":
            print("\n--- Consultar Extrato ---")
            cpf_usuario = input("Digite o CPF do titular da conta para consulta do extrato: ")
            conta_selecionada = selecionar_conta(banco, cpf_usuario)

            if conta_selecionada:
                operacoes.exibir_extrato(conta_selecionada)
            else:
                print("Não foi possível exibir o extrato.")
        
        elif opcao == "6":
            print("\nSaindo do sistema... Obrigado por usar nossos serviços!")
            break
        
        else:
            print("Opção inválida! Por favor, tente novamente.")

if __name__ == "__main__":
    sistema_bancario()