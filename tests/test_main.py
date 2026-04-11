import os
import json
import pytest
from src.main import cadastrar_animal, listar_animais, marcar_adotado, ARQUIVO_DADOS

def setup_function():
    # Limpar arquivo de dados antes de cada teste
    if os.path.exists(ARQUIVO_DADOS):
        os.remove(ARQUIVO_DADOS)

def teardown_function():
    # Limpar arquivo de dados após cada teste
    if os.path.exists(ARQUIVO_DADOS):
        os.remove(ARQUIVO_DADOS)

def test_cadastrar_animal():
    animal = cadastrar_animal("Rex", "Cachorro", 3, "Muito dócil")
    assert animal["nome"] == "Rex"
    assert animal["especie"] == "Cachorro"
    assert animal["adotado"] == False
    
    # Verificar no arquivo
    with open(ARQUIVO_DADOS, 'r', encoding='utf-8') as f:
        dados = json.load(f)
    assert len(dados) == 1
    assert dados[0]["nome"] == "Rex"

def test_listar_animais():
    cadastrar_animal("Mimi", "Gato", 2, "Brincalhona")
    cadastrar_animal("Thor", "Cachorro", 5, "Guarda")
    dados = listar_animais()
    assert len(dados) == 2

def test_marcar_adotado():
    cadastrar_animal("Bolinha", "Gato", 1, "Pequeno")
    # No inicio é não-adotado
    dados = listar_animais()
    assert dados[0]["adotado"] == False
    
    # Marcar como adotado
    sucesso = marcar_adotado(dados[0]["id"])
    assert sucesso == True
    
    # Verificar novamente
    dados_atualizados = listar_animais()
    assert dados_atualizados[0]["adotado"] == True
