import requests
from loguru import logger
import pandas as pd
import json

def get_api_token_local():

    return "OmPFkOjcwWrH62MrXzQDUjz6ClW04RKXSrBqxTqr"

def get_user_token_local():
    return "IBYFZYPmHugD0oxtGOwGt5pHj5Lc7rsmdN2FP9lP"

def get_glpi_host_local():

    return 'http://localhost:8081/'




def get_glpi_host_aws():

    return 'https://systemframe.verdanadesk.com/'

def get_api_token_aws():

    return "c9v5vpT0ubNf1TR7clLRqasacvHVZxL9u4DKUJU9"

def get_user_token_aws():
    return 'QhN3YpNgIzIaLcRhmVhg0X54ZBZHeQ6JF6op9zil'




def get_auth_token_aws(url=get_glpi_host_aws(), token=get_user_token_aws() , app_token=get_api_token_aws()):
    headers = {
        'Authorization': f'user_token {token}',
        'App-Token': app_token
    }

    logger.debug(f"Sending request: {headers}")


    # Make the GET request with query string parameters
    response = requests.get(f'{url}apirest.php/initSession', headers=headers)
    
    logger.debug(f"Got response {response.json()}")
    if response.status_code != 200:
        raise Exception(f'Failed to receive authentication token from GLPi. Status code: {response.status_code}')
    
    try:
        response_data = response.json()
    except ValueError:
        raise Exception('Failed to parse response from GLPi when getting authentication token.')

    if 'session_token' not in response_data:
        raise Exception('Failed to process response received from GLPi. No session token found.')

    return response_data['session_token']




def get_auth_token_local(url=get_glpi_host_local(), token=get_user_token_local() , app_token=get_api_token_local()):
    headers = {
        'Authorization': f'user_token {token}',
        'App-Token': app_token
    }

    logger.debug(f"Sending request: {headers}")


    # Make the GET request with query string parameters
    response = requests.get(f'{url}apirest.php/initSession', headers=headers)
    
    logger.debug(f"Got response {response.json()}")
    if response.status_code != 200:
        raise Exception(f'Failed to receive authentication token from GLPi. Status code: {response.status_code}')
    
    try:
        response_data = response.json()
    except ValueError:
        raise Exception('Failed to parse response from GLPi when getting authentication token.')

    if 'session_token' not in response_data:
        raise Exception('Failed to process response received from GLPi. No session token found.')

    return response_data['session_token']

def get_datas_users():
    api_url = "https://systemframe.verdanadesk.com/apirest.php/User"
    session_token = get_auth_token_aws() 
    headers = {
        'Session-Token': session_token,
        'App-Token': get_api_token_aws()
    }
    users = []
    offset = 0
    page = 1
    per_page = 50

    # Fazer a requisição GET para buscar todos os problemas
    while len(users)<100:
        params = {
            'start':offset,
            'limit':per_page
        }
        response = requests.get(f"{api_url}?range=0-99999", headers=headers,params=params)

        if response.status_code == 200 or response.status_code == 206:
            data = response.json()
            if not data:
                break
            users.extend(data)
            if len(data) < per_page:
                break
            page += 1
        else:
            print(f"Falha ao buscar problemas. Status Code: {response.status_code}")
            print("Detalhes do erro:", response.text)
            break

    return users

def set_datas_users():
    users = get_datas_users()
    session_token = get_auth_token_local() 
    headers = {
        'Session-Token': session_token,
        'App-Token': get_api_token_local()
    }
    for row in users:
        glpi_data ={"input": {
            "name": row["name"],
            "phone": row["phone"],
            "firstname": row["firstname"],
            "locations_id": row["locations_id"],
            "use_mode": row["use_mode"],
            "is_active": row["is_active"],
            "auths_id": row["auths_id"],
            "authtype": row["authtype"],
            "use_mode": row["use_mode"],
            "date_mod":row['date_mod'],
            "date_creation":row['date_creation'],
            "entities_id":row["entities_id"],
            "usertitles_id":row["usertitles_id"],

        }}
        pass        
        logger.debug(f"Request: {json.dumps(glpi_data)}")
        try:
            response = requests.post(f'{get_glpi_host_local()}/apirest.php/User', headers=headers, json=glpi_data)
            if response.status_code == 201:
                logger.debug(f'User created in GLPI: {response.json()}')
            else:
                logger.error("deu erro otario")
                logger.error(response.json())
        except Exception as e:
            pass




print(set_datas_users())