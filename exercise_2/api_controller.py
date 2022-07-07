from flask import request
from flask import Blueprint
import config
import db
import json


urls_blueprint = Blueprint('urls', __name__,)

# database connection, reused for all request, in production this must be a pool
DB_CONN = None


#### ROUTES

#####################################
######       PRODUCT_TYPES      #####
#####################################
### GET
@urls_blueprint.route(f'{config.API_PATH}/product/types', methods=['GET'])
def get_product_types():
    query = "Select id, type from product_types"
    return api_response(200, db.query(DB_CONN, query))



#####################################
######       PRODUCT            #####
#####################################
### POST
@urls_blueprint.route(f'{config.API_PATH}/products', methods=['POST'])
def add_product():
    data = json.loads(request.data, strict=False)

    if check_parameters(["brand", "type", "kcal", "fat", "sugar"], data) == False:
        return api_response(400, "Error some parameters missing")

    if data["fat"] < 0 or data["fat"] > 100:
        return api_response(400, "kcal parameter not valid")
    
    if data["sugar"] < 0 or data["sugar"] > 100:
        return api_response(400, "sugar parameter not valid")
        
    query = f'INSERT INTO products (brand, product_type_id, kcal, fat, sugar) \
              VALUES ("{ data["brand"] }", "{ data["type"] }", "{ data["kcal"] }", \
              "{ data["fat"] }", "{ data["sugar"] }");'
    
    db_response = db.insert(DB_CONN, query)
    if isinstance(db_response, str):
        return api_response(400, db_response)
    else: 
        query = f'SELECT * FROM products WHERE rowid={db_response}'
        return api_response(200, db.query(DB_CONN, query))
    
### GET
@urls_blueprint.route(f'{config.API_PATH}/products', methods=['GET'])
def get_products():
    query = "Select * from products"
    return json.dumps(db.query(DB_CONN, query))

### PUT
@urls_blueprint.route(f'{config.API_PATH}/products/<id>', methods=['PUT'])
def update_product(id):
    data = json.loads(request.data, strict=False)

    if check_parameters(["brand", "type", "kcal", "fat", "sugar"], data) == False:
        return api_response(400, "Error some parameters missing")
        
    query = f'UPDATE products SET \
              brand="{ data["brand"] }", \
              product_type_id="{ data["type"] }", \
              kcal="{ data["kcal"] }", \
              fat="{ data["fat"] }", \
              sugar= "{ data["sugar"] }" \
              WHERE id={id}'
    
    db_response = db.update(DB_CONN, query)
    if db_response == True :
        query = f'SELECT * FROM products WHERE rowid={id}'
        return api_response(200, db.query(DB_CONN, query))
    else: 
        return api_response(400, db_response)



#####################################
######       SUPERMARKET        #####
#####################################
### GET
@urls_blueprint.route(f'{config.API_PATH}/supermarkets', methods=['GET'])
def get_supermarket():
    query = "SELECT * from supermarkets"
    return json.dumps(db.query(DB_CONN, query))

@urls_blueprint.route(f'{config.API_PATH}/supermarkets/<id>/products', methods=['GET'])
def get_supermarket_products(id):
    query = f'SELECT p.price, prod.* from supermarkets s INNER JOIN product_prices p \
            ON s.id=p.supermarket_id INNER JOIN products prod ON prod.id=p.product_id \
            WHERE s.id={id}'
    return json.dumps(db.query(DB_CONN, query))

### POST
@urls_blueprint.route(f'{config.API_PATH}/supermarkets', methods=['POST'])
def add_supermarkets():
    data = json.loads(request.data, strict=False)

    if check_parameters(["name", "direction", "opening_hours"], data) == False:
        return api_response(400, "Error some parameters missing")
        
    query = f'INSERT INTO supermarkets (name, direction, opening_hours) \
              VALUES ("{ data["name"] }", "{ data["direction"] }", "{ data["opening_hours"] }");'
    
    db_response = db.insert(DB_CONN, query)
    if isinstance(db_response, str):
        return api_response(400, db_response)
    else: 
        query = f'SELECT * FROM supermarkets WHERE rowid={db_response}'
        return api_response(200, db.query(DB_CONN, query))

#####################################
######       PRICES             #####
#####################################
### POST
@urls_blueprint.route(f'{config.API_PATH}/product_prices', methods=['POST'])
def add_price():
    data = json.loads(request.data, strict=False)

    if check_parameters(["product_id", "supermarket_id", "price"], data) == False:
        return api_response(400, "Error some parameters missing")

    query = f'INSERT INTO product_prices (product_id, supermarket_id, price) \
              VALUES ("{ data["product_id"] }", "{ data["supermarket_id"] }", "{ data["price"] }");'

    db_response = db.insert(DB_CONN, query)
    if isinstance(db_response, str):
        return api_response(400, db_response)
    else: 
        query = f'SELECT rowid AS id, * FROM product_prices WHERE rowid={db_response}'
        return api_response(200, db.query(DB_CONN, query))


############## utils
def check_parameters(parameters, data):
    for p in parameters:
        if data.get(p) == None:
            return False
    return True

def api_response(code, msg):
    return json.dumps(msg), code, {'ContentType':'application/json'}
