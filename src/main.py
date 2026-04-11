import json
import os

ARQUIVO_DADOS = "animais.json"

def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def cadastrar_animal(nome, especie, idade, observacao):
    dados = carregar_dados()
    novo_animal = {
        "id": len(dados) + 1,
        "nome": nome,
        "especie": especie,
        "idade": idade,
        "observacao": observacao,
        "adotado": False
    }
    dados.append(novo_animal)
    salvar_dados(dados)
    print(f"\nAnimal '{nome}' cadastrado com sucesso!")
    return novo_animal

def listar_animais():
    dados = carregar_dados()
    if not dados:
        print("\nNenhum animal cadastrado no sistema.")
        return dados
    print("\n--- Lista de Animais ---")
    for animal in dados:
        status = "Adotado" if animal["adotado"] else "Disponível"
        print(f"[{animal['id']}] Nome: {animal['nome']} | Espécie: {animal['especie']} | Idade: {animal['idade']} | Status: {status}")
    return dados

def marcar_adotado(id_animal):
    dados = carregar_dados()
    for animal in dados:
        if animal["id"] == id_animal:
            animal["adotado"] = True
            salvar_dados(dados)
            print(f"\nAnimal '{animal['nome']}' foi marcado como ADOTADO!")
            return True
    print("\nAnimal não encontrado.")
    return False

def menu():
    while True:
        print("\n=== Sistema de Registro para Adoção de Animais ===")
        print("1. Cadastrar novo animal")
        print("2. Listar animais")
        print("3. Registrar adoção")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            nome = input("Nome do animal: ")
            especie = input("Espécie (ex: Cachorro, Gato): ")
            try:
                idade = int(input("Idade (em anos): "))
            except ValueError:
                print("Por favor, digite uma idade válida em números inteiros.")
                continue
            obs = input("Observações: ")
            cadastrar_animal(nome, especie, idade, obs)
        elif opcao == "2":
            listar_animais()
        elif opcao == "3":
            try:
                id_animal = int(input("Digite o ID do animal adotado: "))
                marcar_adotado(id_animal)
            except ValueError:
                print("ID inválido. Apenas números.")
        elif opcao == "4":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
