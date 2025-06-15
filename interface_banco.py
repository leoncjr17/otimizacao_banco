limite_saques = 3
valor_max_saque = 500
saques_realizados = 0
saldo = 0
extrato = []

def registrar_saque(valor):
    extrato.append(("Saque", valor))

def registrar_deposito(valor):
    extrato.append(("Depósito", valor))

menu = """
        Bem-vindo, usuário. Escolha a operação que deseja realizar:         

1 - Depositar
2 - Sacar
3 - Extrato
4 - Sair

"""

while True:
    print(menu)
    
    try:
        operacao = int(input("Digite a opção desejada: "))
    except ValueError:
        print("Entrada inválida! Digite um número entre 1 e 4.")
        continue

    if operacao == 1:
        valor_deposito = float(input("Digite o valor de depósito: "))
        saldo += valor_deposito
        registrar_deposito(valor_deposito)
        print(f"Depósito de R${valor_deposito:.2f} realizado com sucesso.")
        if valor_deposito == 0:
            print("Valor de depósito inválido, tente novamente.")
            continue
        
    elif operacao == 2:
        if saques_realizados < limite_saques:
            valor_saque = float(input("Digite o valor de saque: "))
            if valor_saque <= valor_max_saque and valor_saque <= saldo:
                saldo -= valor_saque
                saques_realizados += 1
                registrar_saque(valor_saque)
                print(f"Saque de R${valor_saque:.2f} realizado com sucesso.")
            else:
                print("Valor de saque inválido.")
        else:
            print("Limite de saques diários atingido.")
            
    elif operacao == 3:
        print("\n=== EXTRATO ===")
        if extrato:
            for tipo, valor in extrato:
                print(f"{tipo}: R$ {valor:.2f}")
        else:
            print("Nenhuma operação realizada.")
        print(f"\nSaldo final: R$ {saldo:.2f}")
        
    elif operacao == 4:
        print("Obrigado por usar nossos serviços. Até mais")
        break

    else:
        print("Operação inválida! Digite um número entre 1 e 4.")