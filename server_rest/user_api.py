import requests
import json
import jsonpath

# Global
url = 'https://serverest.dev/usuarios/'
data_set = {"nome": "EU QA Teste", "email": "qa@qa.com.br", "password": "teste", "administrador": "true"}
data_set_update = {"nome": "EU QA Teste 2", "email": "qa@qa.com.br", "password": "teste", "administrador": "true"}

# functions
def load_file():
    file_body = open("C:/repositories/python_api_testing/server_rest/body.json", "r")
    input_file = file_body.read()

    return input_file

def create_user(url, input_file, data_set):
    # Replace values
    body_string = replace_values(input_file, data_set)
    
    body_json = json.loads(body_string)

    print(body_json)

    # sending request
    response = requests.post(url, data=body_json)

    # validation response code
    assert response.status_code == 201

    # geting user ID
    json_response = json.loads(response.text)
    user_id = jsonpath.jsonpath(json_response, '_id')
    user_id = user_id[0]
    print(f'USER ID: {user_id}')

    return user_id

def read_user(url, user_id, data_set=None):
    # Get Request
    response = requests.get(url + user_id)
    print(response.text)

    if response.status_code == 200:

        # Asserts
        json_response = json.loads(response.text)
        assert json_response['nome'] == data_set['nome']
        assert json_response['email'] == data_set['email']
        assert json_response['password'] == data_set['password']
        assert json_response['administrador'] == data_set['administrador']
        assert json_response['_id'] == user_id

    elif response.status_code == 400:
        assert response.status_code == 400

        json_response = json.loads(response.text)

        # Assert
        message = jsonpath.jsonpath(json_response, 'message')
        message = message[0]
        assert message == "Usuário não encontrado"
        print(message)

def update_user(url, input_file, data_set, user_id):
    body_string = replace_values(input_file, data_set)
    body_json = json.loads(body_string)

    # sending request
    response = requests.put(url+user_id, data=body_json)
    print(response.text)

    # Assertion
    print(response.status_code)
    assert response.status_code == 200

    read_user(url,user_id,data_set)

    return user_id

def delete_user(url, user_id):
    # Delete request
    response = requests.delete(url + user_id)

    json_response = json.loads(response.text)

    # Assert
    message = jsonpath.jsonpath(json_response, 'message')
    message = message[0]
    assert message == 'Registro excluído com sucesso'
    print(message)

    # Executing other Get to confer
    read_user(url, user_id) 
    
def replace_values(input_file, data_set):
    input_file = input_file.replace("_nome",data_set["nome"])
    input_file = input_file.replace("_email",data_set["email"])
    input_file = input_file.replace("_password",data_set["password"])
    input_file = input_file.replace("_administrador",data_set["administrador"])
    # print(input_file)

    return input_file

    
# Execution
input_file = load_file()

# Create 
user_id = create_user(url, input_file, data_set)

# Read 
read_user(url, user_id, data_set)

# Update
update_user(url, input_file, data_set_update, user_id)

# Delete 
delete_user(url,user_id)


