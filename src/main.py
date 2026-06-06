def executar():
    print("Digite SAIR para encerrar o programa.")

    while True:
        pergunta = input("Faça sua pergunta: ").strip()

        if pergunta.upper() == "SAIR":
            break

        if not pergunta:
            print("Erro: a pergunta não pode ser vazia.")
        else:
            print(f"Você digitou: {pergunta}")


if __name__ == "__main__":
    executar()
