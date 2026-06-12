# Registro de Animais para Adoção

> 🌐 **Aplicação publicada:** https://adocao-animais.onrender.com

Um sistema em Python para o cadastro e controle de adoção de animais, com **interface web (Flask)** e **interface CLI**. O projeto demonstra boas práticas de desenvolvimento: testes automatizados, integração com API pública, persistência em banco de dados relacional (PostgreSQL/Supabase), pipeline de CI no GitHub Actions e deploy em nuvem.

## O que tem de novo nesta entrega (Etapa Final)

- 🗄️ **Persistência em banco de dados**: SQLAlchemy + PostgreSQL (Supabase) substituindo o arquivo JSON.
- 🧩 **Modelos ORM** (`src/models.py`): modelo `Animal` mapeado via SQLAlchemy com todos os campos do sistema.
- 🔌 **Integração com API pública**: [The Dog API](https://thedogapi.com) — ao cadastrar um cachorro com raça, o sistema busca automaticamente temperamento, expectativa de vida, peso e origem.
- 🌐 **Interface Web** com Flask, publicada online via Render.
- 🧪 **Testes de integração Flask** (`tests/test_main.py`) cobrindo os endpoints da aplicação com banco de dados real (criado e destruído por fixture).
- 🚀 **Deploy contínuo** via Render usando `render.yaml`.

## Como Executar Localmente

### Pré-requisitos
```bash
pip install -r requirements.txt
```

Configure a variável de ambiente `DATABASE_URL` com a string de conexão do seu banco PostgreSQL (ex: Supabase):

```bash
# .env
DATABASE_URL=postgresql://usuario:senha@host:porta/banco
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
5. **Consulta de Raça**: endpoint `/raca?nome=...` que consulta diretamente a The Dog API e retorna JSON.
6. **Persistência**: todos os dados são salvos em banco de dados PostgreSQL via SQLAlchemy (Supabase em produção).

## Como Testar

```bash
pytest tests/ -v
```

Os testes cobrem:
- `tests/test_main.py` — **testes de integração Flask**: verifica os endpoints `/cadastrar`, `/`, `/adotar/<id>` e `/health` com banco de dados real (criado e destruído por fixture `pytest`).
- `tests/test_integration_api.py` — **testes de integração da API externa**: valida a comunicação com a The Dog API (mockada com `responses`), incluindo: resposta de sucesso, raça inexistente, falha de rede, fluxo end-to-end de cadastro enriquecido.

## Estrutura do Projeto

```
adocao-animais/
├── src/
│   ├── main.py             # CLI + lógica de negócio
│   ├── models.py           # Modelos SQLAlchemy (Animal) + configuração do banco
│   ├── api_client.py       # Cliente da The Dog API
│   ├── app.py              # Interface web Flask
│   └── templates/          # HTML (Jinja2)
├── tests/
│   ├── test_main.py            # Testes de integração Flask (endpoints + DB)
│   └── test_integration_api.py # Testes de integração com a The Dog API
├── .github/workflows/          # CI (GitHub Actions)
├── .env                    # DATABASE_URL e outras variáveis (não versionado)
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
