from flask import Flask, Response
from flask_restful import Api
from datetime import datetime
from collections import OrderedDict
import json
import operator

ARQUIVO_PEDIDOS = 'pedidos.json'

app = Flask(__name__)
api = Api(app)

def le_arquivo_pedidos():
    try:
        with open(ARQUIVO_PEDIDOS) as arquivo_pedidos:
            dados_pedidos = json.load(arquivo_pedidos)  
    except FileNotFoundError:
            return Response(json.dumps({'Erro': 'O arquivo não foi encontrado!'},
                                        status=404))
    else:
        return dados_pedidos


@app.route('/criarpedido/<string:cliente>/<string:produto>/<float:valor>', methods=['POST', 'GET'])
def post_pedido(cliente, produto, valor):
    dados_pedidos = le_arquivo_pedidos()
        
    id = dados_pedidos['nextId']
    next_id = id + 1
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    novo_pedido = { 
        'id': id,
        'cliente': cliente,
        'produto': produto,
        'valor': valor,
        'entregue': False,
        'timestamp': timestamp
    }

    try:
        with open(ARQUIVO_PEDIDOS, 'r+') as arquivo_pedidos:
            dados_pedidos = json.load(arquivo_pedidos)
            dados_pedidos['nextId'] = next_id              # Atualiza valor do id
            dados_pedidos['pedidos'].append(novo_pedido)    # Adiciona novo pedido no final da lista
            arquivo_pedidos.seek(0)                    # Vai pro começo do arquivo
            json.dump(dados_pedidos, arquivo_pedidos, indent=4)
            arquivo_pedidos.truncate()                 # Remove oque tinha antes no arquivo
    except:
        return Response(json.dumps({'Erro': 'Não foi possível salvar o novo pedido!'}),
                                    status=500)
    else:
        return Response(json.dumps(novo_pedido, indent=4), status=200)


@app.route('/')
def welcome():
    return "<p>Welcome to the delivery API</p>"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')