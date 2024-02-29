# Investapp-API

## Descrição
Este é um projeto desenvolvido com FastAPI e MongoDB para manter um registro de operações de compra e venda de ações.

## Pré-requisitos
Certifique-se de ter o Python instalado em sua máquina. Além disso, crie um ambiente virtual e instale as dependências do projeto usando:

```bash
pip install -r requirements.txt
```
## Configuração do Banco de Dados

Crie o arquivo .env e configure as variáveis de ambiente para o MongoDB.

```bash
MONGODB_URI=connection_string
DB_NAME=sua_base_de_dados
```
## Executando o Projeto

Para iniciar o servidor, execute o seguinte comando:

```bash
uvicorn main:app --reload
```
O servidor estará disponível em http://localhost:8000.

Endpoints

prefixo "/operacoes"

    Cadastrar Operação: POST /cadastrar
    Listar Operações: GET /list
    Obter Operação: GET /operacao/{operacao_id}
    Obter Operação pelo codigo da ação: GET /operacao/cod/{cod_acao}
    Obter média da operação do tipo 'compra': GET /operacao/media_compras
    Obter média da operação do tipo 'venda': GET /operacao/media_vendas
    
Certifique-se de revisar a documentação da API em http://localhost:8000/docs para obter detalhes sobre como usar cada endpoint.

## Licença
Este projeto é licenciado sob a [Licença MIT](./LICENSE.md).
