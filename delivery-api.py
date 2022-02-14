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
    with open(ARQUIVO_PEDIDOS) as arquivo_pedidos:
        dados_pedidos = json.load(arquivo_pedidos)  
    return dados_pedidos

def verifica_existencia_produto(produto, pedidos):
    for pedido in pedidos:
        if pedido is not None and produto == pedido['produto']:
            return True
    return False


@app.route('/criarpedido/<string:cliente>/<string:produto>/<float:valor>', methods=['POST', 'GET'])
def post_pedido(cliente, produto, valor):
    try:
        dados_pedidos = le_arquivo_pedidos()
    except FileNotFoundError:
        return Response(json.dumps({'Erro': 'O arquivo não foi encontrado!'}),
                        status=404)

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
            dados_pedidos['nextId'] = next_id              
            dados_pedidos['pedidos'].append(novo_pedido)   
            arquivo_pedidos.seek(0)                    
            json.dump(dados_pedidos, arquivo_pedidos, indent=4)
            arquivo_pedidos.truncate()                 
    except:
        return Response(json.dumps({'Erro': 'Não foi possível salvar o novo pedido!'}),
                        status=500)
    else:
        return Response(json.dumps(novo_pedido, indent=4), status=200)


@app.route('/atualizarpedido/<int:id>/<string:cliente>/<string:produto>/<float:valor>/<entregue>', 
            methods=['PUT', 'GET'])
def put_produto(id, cliente, produto, valor, entregue):
    try:
        dados_pedidos = le_arquivo_pedidos()  
    except FileNotFoundError:
            return Response(json.dumps({'Erro': 'O arquivo não foi encontrado!'}),
                            status=404)

    if not verifica_existencia_produto(produto, dados_pedidos['pedidos']):
        return Response(json.dumps({'Erro': 'O produto informado não existe!'}),
                        status=404)

    pedido_atualizado = {}
    for pedido in dados_pedidos['pedidos']:
        if pedido is not None and pedido['id'] == id:       
            pedido['produto'] = produto
            pedido['cliente'] = cliente
            pedido['valor'] = valor
            pedido['entregue'] = entregue
            pedido_atualizado = pedido
            break

    if not pedido_atualizado:
        return Response(json.dumps({'Erro': 'Não foi encontrado um pedido com o id informado!'}), 
                        status=404)

    try:
        with open(ARQUIVO_PEDIDOS , 'r+') as arquivo_pedidos:
            json.dump(dados_pedidos, arquivo_pedidos, indent=4)
            arquivo_pedidos.truncate()
    except:
        return Response(json.dumps({'Erro': 'Não foi possível salvar as alterações.'}),
                        status=500)
    else:
        return Response(json.dumps(pedido_atualizado, indent=4),
                        status=200)


@app.route('/atualizarstatus/<int:id>/<entregue>', methods=['PUT', 'GET'])
def put_status_pedido(id, entregue):
    try:
        dados_pedidos = le_arquivo_pedidos()  
    except FileNotFoundError:
            return Response(json.dumps({'Erro': 'O arquivo não foi encontrado!'}),
                            status=404)
        
    if entregue.lower() == 'true':
        entregue = True
    else:
        entregue = False

    pedido_atualizado = {}
    for pedido in dados_pedidos['pedidos']:
        if pedido is not None and pedido['id'] == id:
            pedido['entregue'] = entregue
            pedido_atualizado = pedido
            break

    if not pedido_atualizado:
        return Response(json.dumps({'Erro': 'Não foi encontrado um pedido com o id informado!'}), 
                        status=404)
    
    try:
        with open(ARQUIVO_PEDIDOS, 'r+') as arquivo_pedidos:
            json.dump(dados_pedidos, arquivo_pedidos, indent=4)
            arquivo_pedidos.truncate()
    except:
        return Response(json.dumps({'Erro': 'Não foi possível salvar a alteração!'}),
                        status=500)
    else:
        return Response(json.dumps(pedido_atualizado), status=200)


@app.route('/excluirpedido/<int:id>', methods=['DELETE', 'GET'])          
def delete_produto(id):
    try:
        dados_pedidos = le_arquivo_pedidos()  
    except FileNotFoundError:
            return Response(json.dumps({'Erro': 'O arquivo não foi encontrado!'}),
                            status=404)

    pedido_removido = {}
    for pedido in dados_pedidos['pedidos']:
        if pedido is not None and pedido['id'] == id:
            pedido_removido = pedido
            dados_pedidos['pedidos'].remove(pedido)
            break
        
    if not pedido_removido:
        return Response(json.dumps({'Erro': 'Não foi encontrado um pedido com o id informado!'}), 
                                    status=404)

    try:
        with open(ARQUIVO_PEDIDOS, 'r+') as arquivo_pedidos:
            json.dump(dados_pedidos, arquivo_pedidos, indent=4)
            arquivo_pedidos.truncate()
    except:
        return Response(json.dumps({'Erro': 'Não foi possível excluir o pedido!'}),
                        status=500)
    else:
        return Response(json.dumps(pedido_removido), status=200)


@app.route('/pedido/<int:id>')
def get_produto(id):
    try:
        dados_pedidos = le_arquivo_pedidos()  
    except FileNotFoundError:
            return Response(json.dumps({'Erro': 'O arquivo não foi encontrado!'}),
                            status=404)

    pedido_consultado = {}  
    for pedido in dados_pedidos['pedidos']:
        if pedido is not None and pedido['id'] == id:
            pedido_consultado = pedido
            break

    if not pedido_consultado:
        return Response(json.dumps({'Erro': 'Não foi encontrado um pedido com o id informado!'}), 
                                    status=404)

    return Response(json.dumps(pedido_consultado), status=200)


@app.route('/pedidoscliente/<string:cliente>')
def get_pedidos_cliente(cliente):
    try:
        dados_pedidos = le_arquivo_pedidos()  
    except FileNotFoundError:
            return Response(json.dumps({'Erro': 'O arquivo não foi encontrado!'}),
                            status=404)
    
    total_pedidos = 0.0
    for pedido in dados_pedidos['pedidos']:
        if pedido is not None and 'cliente' in pedido:
            if pedido['cliente'] == cliente and pedido['entregue'] == True:
                total_pedidos += pedido['valor']
    
    return Response(json.dumps({'total': total_pedidos}), status=200)


@app.route('/totalpedidos/<string:produto>')
def get_total_produto(produto):
    try:
        dados_pedidos = le_arquivo_pedidos()  
    except FileNotFoundError:
            return Response(json.dumps({'Erro': 'O arquivo não foi encontrado!'}),
                            status=404)

    total = 0.0
    for pedido in dados_pedidos['pedidos']:
        if pedido is not None and pedido['produto'] == produto and pedido['entregue'] == True:
            total += pedido['valor']
    
    return Response(json.dumps({'total': total}), status=200)


@app.route('/produtosmaisvendidos')
def get_produtos_mais_vendidos():
    try:
        dados_pedidos = le_arquivo_pedidos()  
    except FileNotFoundError:
            return Response(json.dumps({'Erro': 'O arquivo não foi encontrado!'}),
                            status=404)
    else:
        produtos_vendidos = {}
        
        for pedido in dados_pedidos['pedidos']:
            if pedido is not None:
                produto = pedido['produto']

                if produto in produtos_vendidos and pedido['entregue'] == True:
                    produtos_vendidos[produto] += 1
                elif not (produto in produtos_vendidos) and pedido['entregue'] == True:
                    produtos_vendidos[produto] = 1   
        
        tuplas_ordenadas_produto = sorted(produtos_vendidos.items(), 
                                          key=operator.itemgetter(1), 
                                          reverse=True)
        
        produtos_ordenados = OrderedDict()
        for produto, quantidade in tuplas_ordenadas_produto:
            produtos_ordenados[produto] = quantidade

        return Response(json.dumps(produtos_ordenados, indent=4), status=200)

@app.route('/')
def welcome():
    return "<p>Welcome to the delivery API</p>"


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')