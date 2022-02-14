# Delivery API 🏍️

## O que é?
A Delivery API é uma API em Python que gerencia os pedidos de clientes de um delivery. Possui endpoints para criação, atualização, exclusão e consulta de pedidos.

## Tecnologias Utilizadas
<div style="display: inline">
  <img align="center" alt="python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img align="center" alt="flask" src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
  <img align="center" alt="docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white" />
</div><br/>

## Backlog de Atividades
Foi elaborado um backlog com as tarefas necessárias para o desenvolvimento da API. Para cada tarefa foi criada uma issue, que possui descrição, prioridade e critérios de aceitação. Esse backlog está organizado em ordem de excecução de tarefas pode ser encontrado nos [projects](https://github.com/Gabrielle-Ribeiro/delivery-api/projects/1) desse repositório. 

## Como rodar a delivery api?

### Pré-requisitos
A Delivery API utiliza o docker e docker-compose para garantir um ambiente de desenvolvimento consistente. Então tudo o que você precisa em suas ferramentas de desenvolvimento para executar a Delivery API é o [Docker](https://www.docker.com/) e o [Docker-Compose](https://docs.docker.com/compose/).
Para instalar essas ferramentas, basta seguir o guia de instruções de suas documentações referente ao seu sistema operacional.
  - [Docker para Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
  - [Docker para Debian](https://docs.docker.com/engine/install/debian/)
  - [Docker Compose](https://docs.docker.com/compose/install/) (verificar seu sistema operacional)

### Execução
Para rodar a Delivery API no seu computador você precisa:

  - Clonar esse repositório:
  ```
  git clone https://github.com/Gabrielle-Ribeiro/delivery-api.git
  ```
  
  - Navegar até a pasta do repositório:
  ```
  cd delivery-api
  ```
  
  - Rodar o docker-compose:
  ```
  docker-compose up
  ```
  Se você receber algum erro de ```permissão negada``` ou ```permission denied```, tente executar o comando com sudo.
  ```
  sudo docker-compose up
  ```
  
  - Voilà! Seu terminal irá informar em qual porta está sendo executada a Delivery API. Agora basta acessar essa rota em seu navegador.
  
## Endpoints da Delivery API
  
Para acessar os endpoints dessa API, basta digitar em seu navegador a porta informada na etapa anterior + alguma rota entre as apresentadas a seguir. <br>

**Atenção:** Para parâmetros que em sua escrita possuem espaços entre palavras, basta substituir o parâmetro com espaço entre palavras ou substituindo o espaço por %20. <br> *Exemplo:* para substituir um parâmetro produto por Camarão Internacional, basta escrever na rota ```Camarão Internacional``` ou ```Camarão%20Internacional```.
  
  
### Endpoint para criar um pedido
Rota: 
```
/criarpedido/<string:cliente>/<string:produto>/<float:valor>
```
  
Parâmetros:
- ```<string:cliente>``` deve ser substituído pelo nome de um cliente.
- ```<string:produto>``` deve ser substituído pelo nome de um produto.
- ```<float:valor>``` deve ser substituído pelo valor do produto. Esse valor deve ser necessariamente um número de ponto flutuante.

Retorno:
- Retorna um json com o pedido criado.
  
### Endpoint para atualizar um pedido
Rota: 
```
/atualizarpedido/<int:id>/<string:cliente>/<string:produto>/<float:valor>/<entregue>
```
  
Parâmetros:
- ```<int:id>``` deve ser substituído pelo id de um pedido.
- ```<string:cliente>``` deve ser substituído pelo nome de um cliente.
- ```<string:produto>``` deve ser substituído pelo nome de um produto.
- ```<float:valor>``` deve ser substituído pelo valor do produto. Esse valor deve ser necessariamente um número de ponto flutuante.
- ```<entregue>``` deve ser substituído por True ou False.

Retorno:
- Retorna um json com o pedido atualizado.

### Endpoint para atualizar o status de entrega de um pedido
Rota: 
```
/atualizarstatus/<int:id>/<entregue>
```
  
Parâmetros:
- ```<int:id>``` deve ser substituído pelo id de um pedido.
- ```<entregue>``` deve ser substituído por True ou False.
  
Retorno:
- Retorna um json com o pedido atualizado.
  
### Endpoint para excluir um pedido
Rota: 
```
/excluirpedido/<int:id>
```
  
Parâmetros:
- ```<int:id>``` deve ser substituído pelo id de um pedido.

Retorno:
- Retorna um json com o pedido excluído.
  
### Endpoint para consultar um pedido em específico
Rota:
```
/pedido/<int:id>
```
  
Parâmetros:
- ```<int:id>``` deve ser substituído pelo id de um pedido.

Retorno:
- Retorna um json com o pedido solicitado.
  
### Endpoint para consultar o valor total de pedidos já realizados por um mesmo cliente
Rota:
```
/pedidoscliente/<string:cliente>
```
  
Parâmetros:
- ```<string:cliente>``` deve ser substituído pelo nome de um cliente.

Retorno:
- Retorna um json com o valor total de pedidos realizados pelo cliente.

### Endpoint para consultar o valor total de pedidos já realizados para um determinado produto
Rota:
```
/totalpedidos/<string:produto>
```
  
Parâmetros:
- ```<string:produto>``` deve ser substituído pelo nome de um produto.

Retorno:
- Retorna um json com o valor total de pedidos realizados para o produto informado.
 
 
### Endpoint para retornar os produtos mais vendidos e a quantidade de vezes em que estes foram pedidos
Rota:
```
/produtosmaisvendidos
```
  
Parâmetros:
- Não recebe parâmetros

Retorno:
- Retorna um json com o os produtos mais vendidos e suas quantidades em ordem decrescente.
 
