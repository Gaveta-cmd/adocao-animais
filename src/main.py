import json
import os

from src.api_client import buscar_raca, DogApiError

ARQUIVO_DADOS = "animais.json"

def carregar_dados():
    if not os.path.exists(ARQUIVO_DADOS):
        return []
    with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(dados):
    with open(ARQUIVO_DADOS, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def cadastrar_animal(nome, especie, idade, observacao, raca=None):
    dados = carregar_dados()
    novo_animal = {
        "id": len(dados) + 1,
        "nome": nome,
        "especie": especie,
        "idade": idade,
        "observacao": observacao,
        "raca": raca,
        "info_raca": None,
        "adotado": False
    }

    if raca and especie.strip().lower() in ("cachorro", "cao", "cão", "dog"):
        try:
            info = buscar_raca(raca)
            if info:
                novo_animal["info_raca"] = info
                print(f"\nInformacoes da raca '{info['nome']}' carregadas da The Dog API!")
                print(f"  Temperamento: {info['temperamento']}")
                print(f"  Expectativa de vida: {info['expectativa_vida']}")
            else:
                print(f"\nRaca '{raca}' nao encontrada na The Dog API.")
        except DogApiError as exc:
            print(f"\nAviso: nao foi possivel consultar a API ({exc}). Cadastro segue sem enriquecimento.")

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
        linha = f"[{animal['id']}] Nome: {animal['nome']} | Espécie: {animal['especie']} | Idade: {animal['idade']} | Status: {status}"
        if animal.get("raca"):
            linha += f" | Raça: {animal['raca']}"
        print(linha)
        if animal.get("info_raca"):
            print(f"     Temperamento: {animal['info_raca']['temperamento']}")
            print(f"     Expectativa de vida: {animal['info_raca']['expectativa_vida']}")
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

def consultar_raca_cli(raca):
    try:
        info = buscar_raca(raca)
    except DogApiError as exc:
        print(f"\nErro ao consultar API: {exc}")
        return None
    if not info:
        print(f"\nRaca '{raca}' nao encontrada.")
        return None
    print(f"\n--- Informacoes da raca '{info['nome']}' ---")
    print(f"Temperamento: {info['temperamento']}")
    print(f"Expectativa de vida: {info['expectativa_vida']}")
    print(f"Peso: {info['peso']} kg")
    print(f"Origem: {info['origem']}")
    return info

def menu():
    while True:
        print("\n=== Sistema de Registro para Adoção de Animais ===")
        print("1. Cadastrar novo animal")
        print("2. Listar animais")
        print("3. Registrar adoção")
        print("4. Consultar informações de uma raça (The Dog API)")
        print("5. Sair")

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
            raca = input("Raça (opcional, enriquecido via The Dog API para cachorros): ").strip() or None
            cadastrar_animal(nome, especie, idade, obs, raca)
        elif opcao == "2":
            listar_animais()
        elif opcao == "3":
            try:
                id_animal = int(input("Digite o ID do animal adotado: "))
                marcar_adotado(id_animal)
            except ValueError:
                print("ID inválido. Apenas números.")
        elif opcao == "4":
            raca = input("Digite o nome da raça: ").strip()
            consultar_raca_cli(raca)
        elif opcao == "5":
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
