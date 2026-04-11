# Registro de Animais para Adoção

Um sistema simples em Python desenvolvido para o cadastro e controle de adoção de animais. Este projeto tem foco em demonstrar a utilização de boas práticas de desenvolvimento como testes automatizados, persistência em JSON e fluxo no GitHub Actions.

## Como Executar

1. Instale as dependências:
```bash
pip install -r requirements.txt
```

2. Execute o script principal:
```bash
python -m src.main
```

## Como o Sistema Funciona

O projeto é muito simples e focado no essencial para um abrigo:

1. **Início e Dados**: Ao iniciar, ele automaticamente lê os dados já processados (caso tenha) do arquivo secreto `animais.json` para carregar o histórico.
2. **Cadastro**: Quando você seleciona a opção "1", o sistema te questiona as informações mais vitais. Ele cria um ID único sequencial para o animal e insere "Status: Disponível".
3. **Persistência ao vivo**: Cada ação gravada (como adicionar um animal ou alterar um status) é automaticamente escrita de volta no arquivo principal, garantindo que caso o terminal feche, nenhum dado é perdido.
4. **Registro de Adoção**: Ao escolher adotar, o usuário só necessita informar o ID numérico listado. Instantâneamente a bandeira "Status" do animal é modificada e o sistema reescreve a segurança no banco json local.

## Exemplo de Uso do Sistema

Aqui está um exemplo de interação com o sistema que demonstra, passo-a-passo, a navegação entre todas as opções do menu principal:

```text
=== Sistema de Registro para Adoção de Animais ===
1. Cadastrar novo animal
2. Listar animais
3. Registrar adoção
4. Sair
Escolha uma opção: 1
Nome do animal: Rex
Espécie (ex: Cachorro, Gato): Cachorro
Idade (em anos): 3
Observações: Muito dócil, ótimo com crianças

Animal 'Rex' cadastrado com sucesso!

=== Sistema de Registro para Adoção de Animais ===
1. Cadastrar novo animal
2. Listar animais
3. Registrar adoção
4. Sair
Escolha uma opção: 2

--- Lista de Animais ---
[1] Nome: Rex | Espécie: Cachorro | Idade: 3 | Status: Disponível

=== Sistema de Registro para Adoção de Animais ===
1. Cadastrar novo animal
2. Listar animais
3. Registrar adoção
4. Sair
Escolha uma opção: 3
Digite o ID do animal adotado: 1

Animal 'Rex' foi marcado como ADOTADO!

=== Sistema de Registro para Adoção de Animais ===
1. Cadastrar novo animal
2. Listar animais
3. Registrar adoção
4. Sair
Escolha uma opção: 2

--- Lista de Animais ---
[1] Nome: Rex | Espécie: Cachorro | Idade: 3 | Status: Adotado

=== Sistema de Registro para Adoção de Animais ===
1. Cadastrar novo animal
2. Listar animais
3. Registrar adoção
4. Sair
Escolha uma opção: 4
Saindo do sistema...
```

## Como Testar

Para rodar os testes unitários utilizando o pytest:
```bash
pytest tests/
```

## Estrutura do Projeto
- `src/main.py`: Código principal do sistema.
- `tests/test_main.py`: Testes automatizados do sistema.
- `animais.json`: Arquivo de banco de dados gerado automaticamente na execução.

**Autor**: Davi Augusto de Barros Resende Santana da Silva
**RA**: 22505381
