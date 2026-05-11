"""Testes de integracao com a The Dog API.

Validam o fluxo completo: chamada HTTP -> parse da resposta -> enriquecimento
do cadastro. A requisicao externa eh mockada com a biblioteca `responses`
para nao depender da internet no CI.
"""
import os
import json

import pytest
import responses

from src.api_client import buscar_raca, DogApiError, BASE_URL
from src.main import cadastrar_animal, ARQUIVO_DADOS


def setup_function():
    if os.path.exists(ARQUIVO_DADOS):
        os.remove(ARQUIVO_DADOS)


def teardown_function():
    if os.path.exists(ARQUIVO_DADOS):
        os.remove(ARQUIVO_DADOS)


@responses.activate
def test_buscar_raca_retorna_dados_formatados():
    """Quando a API responde com sucesso, a funcao retorna dict normalizado."""
    responses.add(
        responses.GET,
        f"{BASE_URL}/breeds/search",
        json=[{
            "id": 122,
            "name": "Labrador Retriever",
            "temperament": "Gentle, Outgoing, Trusting",
            "life_span": "10 - 12 years",
            "weight": {"metric": "25 - 36"},
            "origin": "Canada, United Kingdom",
        }],
        status=200,
    )

    info = buscar_raca("Labrador")

    assert info is not None
    assert info["nome"] == "Labrador Retriever"
    assert info["temperamento"] == "Gentle, Outgoing, Trusting"
    assert info["expectativa_vida"] == "10 - 12 years"
    assert info["peso"] == "25 - 36"
    assert info["origem"] == "Canada, United Kingdom"


@responses.activate
def test_buscar_raca_retorna_none_quando_nao_encontrada():
    """Lista vazia da API => raca nao encontrada."""
    responses.add(
        responses.GET,
        f"{BASE_URL}/breeds/search",
        json=[],
        status=200,
    )

    assert buscar_raca("RacaInexistente") is None


@responses.activate
def test_buscar_raca_lanca_erro_quando_api_falha():
    """Erro HTTP da API deve virar DogApiError."""
    responses.add(
        responses.GET,
        f"{BASE_URL}/breeds/search",
        json={"error": "internal"},
        status=500,
    )

    with pytest.raises(DogApiError):
        buscar_raca("Labrador")


def test_buscar_raca_retorna_none_para_entrada_vazia():
    """Sem chamar a API, raca vazia => None."""
    assert buscar_raca("") is None
    assert buscar_raca("   ") is None
    assert buscar_raca(None) is None


@responses.activate
def test_cadastro_de_cachorro_enriquece_via_api():
    """Fluxo de integracao end-to-end: cadastra cachorro -> consulta API -> salva enriquecido."""
    responses.add(
        responses.GET,
        f"{BASE_URL}/breeds/search",
        json=[{
            "name": "Poodle",
            "temperament": "Intelligent, Active",
            "life_span": "12 - 15 years",
            "weight": {"metric": "20 - 32"},
            "origin": "Germany, France",
        }],
        status=200,
    )

    animal = cadastrar_animal(
        nome="Bidu",
        especie="Cachorro",
        idade=4,
        observacao="Brincalhao",
        raca="Poodle",
    )

    assert animal["raca"] == "Poodle"
    assert animal["info_raca"] is not None
    assert animal["info_raca"]["nome"] == "Poodle"
    assert animal["info_raca"]["temperamento"] == "Intelligent, Active"

    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        dados = json.load(f)
    assert dados[0]["info_raca"]["nome"] == "Poodle"


@responses.activate
def test_cadastro_de_gato_nao_chama_api():
    """API soh eh chamada para especie Cachorro; outras especies ficam sem info_raca."""
    responses.add(
        responses.GET,
        f"{BASE_URL}/breeds/search",
        json=[{"name": "qualquer"}],
        status=200,
    )

    animal = cadastrar_animal(
        nome="Mimi",
        especie="Gato",
        idade=2,
        observacao="Doce",
        raca="Persa",
    )

    assert animal["info_raca"] is None
    assert len(responses.calls) == 0


@responses.activate
def test_cadastro_continua_quando_api_falha():
    """Se a API estiver fora, o animal ainda eh cadastrado (sem info_raca)."""
    responses.add(
        responses.GET,
        f"{BASE_URL}/breeds/search",
        json={"error": "down"},
        status=503,
    )

    animal = cadastrar_animal(
        nome="Rex",
        especie="Cachorro",
        idade=5,
        observacao="Calmo",
        raca="Labrador",
    )

    assert animal["nome"] == "Rex"
    assert animal["info_raca"] is None
