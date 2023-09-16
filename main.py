from flask import Flask, make_response, jsonify, request 


conexao = "mysql -hcontainers-us-west-156.railway.app -uroot -pyBaVYeOMqLM14T6wq7oQ --port 6411 --protocol=TCP railway" 

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False 

@app.route("/carros", methods = ["GET"])  
def get_cars(): 
    cursor = conexao.cursor() 
    cursor.execute("SELECT * FROM carros")
    meus_carros = cursor.fetchall() 
  
    listaCarros = list()
    for carro in meus_carros:
        listaCarros.append( 
            { 
                "id": carro[0],
                "marca": carro[1],
                "modelo": carro[2],
                "ano": carro[3]
            }
        )

    return make_response( 
        jsonify( 
            mensagem = "Lista de carros",
            carros = listaCarros)
    )

@app.route("/carros/<id>", methods = ["GET"])  
def getIndividual_car(id): 
    cursor = conexao.cursor() 
    sql = f"SELECT * FROM carros WHERE id_carro = {id}"
    cursor.execute(sql)
    meus_carros = cursor.fetchone() 
  
    carroIndividual =  { 
                "id": meus_carros[0],
                "marca": meus_carros[1],
                "modelo": meus_carros[2],
                "ano": meus_carros[3]
            }
    
    return make_response( 
        jsonify( 
            mensagem = "Carro selecionado",
            carro = carroIndividual 
            )
    )

@app.route("/carros", methods = ["POST"]) 
def create_car(): 
    novoCarro = request.json 
    
    cursor = conexao.cursor() 
    sql = f"INSERT INTO carros(marca, modelo, ano) VALUES ('{novoCarro['marca']}', '{novoCarro['modelo']}', '{novoCarro['ano']}')" 
    cursor.execute(sql) 
    conexao.commit() 

    return make_response( 
        jsonify( mensagem = "Carro cadastrado com sucesso" )
    )

@app.route("/carros/<id>", methods = ["PUT"]) 
def update_car(id): 
    atualizaCarro = request.json
    
    cursor = conexao.cursor() 
    sql = f"UPDATE carros SET marca = '{atualizaCarro['marca']}' WHERE id_carro = {id}" 
    cursor.execute(sql) 
    conexao.commit() 

    return make_response( 
        jsonify( mensagem = "Carro atualizado com sucesso" )
    )

@app.route("/carros/<id>", methods = ["DELETE"])
def delete_car(id):  
    cursor = conexao.cursor() 
    sql = f"DELETE FROM carros WHERE id_carro = {id}" 
    cursor.execute(sql) 
    conexao.commit() 

    return make_response( 
        jsonify( mensagem = "Carro deletado" )
    )

app.run()
