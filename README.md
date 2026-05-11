# Registro de Animais para Adoção

> 🌐 **Aplicação publicada:** _adicionar link do Render após o deploy (ver seção [Deploy](#deploy))_

Um sistema em Python para o cadastro e controle de adoção de animais, com **interface web (Flask)** e **interface CLI**. O projeto demonstra boas práticas de desenvolvimento: testes automatizados, integração com API pública, persistência em JSON, pipeline de CI no GitHub Actions e deploy em nuvem.

## O que tem de novo nesta entrega (Etapa Intermediária)

- 🔌 **Integração com API pública**: [The Dog API](https://thedogapi.com) — ao cadastrar um cachorro com raça, o sistema busca automaticamente temperamento, expectativa de vida, peso e origem.
- 🌐 **Interface Web** com Flask, publicada online via Render.
- 🧪 **Testes de integração** validando o consumo da API externa (mockados com `responses`).
- 🚀 **Deploy contínuo** via Render usando `render.yaml`.

## Como Executar Localmente

### Pré-requisitos
```bash
pip install -r requirements.txt
```

### Modo CLI (terminal)
```bash
python -m src.main
```

### Modo Web (Flask)
```bash
python -m src.app
```
Acesse http://localhost:5000

## Como o Sistema Funciona

1. **Cadastro**: cadastra animais com nome, espécie, idade, observações e (opcional) **raça**.
2. **Enriquecimento via API**: se a espécie for "Cachorro" e a raça for informada, o sistema consulta a **The Dog API** e armazena dados extras (temperamento, life span, peso, origem).
3. **Listagem**: mostra todos os animais e seu status (Disponível/Adotado) — exibe também os dados enriquecidos quando houver.
4. **Adoção**: marca um animal como adotado pelo ID.
5. **Consulta de Raça**: nova tela/opção que permite consultar diretamente a The Dog API.
6. **Persistência**: tudo é gravado em `animais.json` automaticamente.

## Como Testar

```bash
pytest tests/ -v
```

Os testes cobrem:
- `tests/test_main.py` — testes unitários do CRUD.
- `tests/test_integration_api.py` — **testes de integração** validando a comunicação com a The Dog API (com mock via `responses`), incluindo: resposta de sucesso, raça inexistente, falha de rede, fluxo end-to-end de cadastro enriquecido.

## Estrutura do Projeto

```
adocao-animais/
├── src/
│   ├── main.py             # CLI + lógica de negócio
│   ├── api_client.py       # Cliente da The Dog API
│   ├── app.py              # Interface web Flask
│   └── templates/          # HTML (Jinja2)
├── tests/
│   ├── test_main.py            # Testes unitários
│   └── test_integration_api.py # Testes de integração
├── .github/workflows/          # CI (GitHub Actions)
├── requirements.txt
├── Procfile                # Para deploy (gunicorn)
├── render.yaml             # Configuração do Render
└── README.md
```

## Deploy

A aplicação é publicada no **Render** (free tier) a cada push na branch `main`.

### Como fazer o deploy (passo a passo)

1. Crie conta gratuita em https://render.com (login com GitHub).
2. No dashboard, clique em **"New +" → "Web Service"**.
3. Conecte e selecione o repositório `adocao-animais`.
4. O Render detecta automaticamente o `render.yaml` — confirme.
5. Aguarde o build (~2 min). Após concluir, o link público estará disponível no topo do painel.
6. Cole o link no topo deste README na seção indicada.

### Endpoints disponíveis no app web

| Rota | Método | Descrição |
|---|---|---|
| `/` | GET | Lista animais cadastrados |
| `/cadastrar` | GET/POST | Formulário de cadastro |
| `/adotar/<id>` | POST | Marca animal como adotado |
| `/raca?nome=...` | GET | Consulta info de raça via The Dog API |
| `/health` | GET | Healthcheck |

## API Pública Integrada

**The Dog API** — https://thedogapi.com — gratuita, sem token obrigatório.

Endpoint usado: `GET https://api.thedogapi.com/v1/breeds/search?q={raça}`

Exemplo de resposta:
```json
[{
  "name": "Labrador Retriever",
  "temperament": "Gentle, Outgoing, Trusting",
  "life_span": "10 - 12 years",
  "weight": { "metric": "25 - 36" },
  "origin": "Canada, United Kingdom"
}]
```

---

**Autor**: Davi Augusto de Barros Resende Santana da Silva
**RA**: 22505381
