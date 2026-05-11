"""Cliente para integracao com The Dog API (https://thedogapi.com).

Permite enriquecer o cadastro de animais com informacoes publicas sobre a raca:
temperamento, expectativa de vida, peso e origem.
"""
import requests

BASE_URL = "https://api.thedogapi.com/v1"
TIMEOUT = 5


class DogApiError(Exception):
    """Erro ao consultar a The Dog API."""


def buscar_raca(nome_raca):
    """Busca informacoes de uma raca de cachorro pelo nome.

    Retorna um dict com {nome, temperamento, expectativa_vida, peso, origem}
    ou None se a raca nao for encontrada.
    """
    if not nome_raca or not nome_raca.strip():
        return None

    try:
        response = requests.get(
            f"{BASE_URL}/breeds/search",
            params={"q": nome_raca.strip()},
            timeout=TIMEOUT,
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise DogApiError(f"Falha ao consultar The Dog API: {exc}") from exc

    resultados = response.json()
    if not resultados:
        return None

    raca = resultados[0]
    return {
        "nome": raca.get("name"),
        "temperamento": raca.get("temperament", "Nao informado"),
        "expectativa_vida": raca.get("life_span", "Nao informado"),
        "peso": (raca.get("weight") or {}).get("metric", "Nao informado"),
        "origem": raca.get("origin") or "Nao informado",
    }
