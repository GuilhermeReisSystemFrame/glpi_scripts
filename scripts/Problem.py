import requests
from loguru import logger
import pandas as pd
import json

# Display the first few rows of the DataFrame
def get_api_token():

    return "OmPFkOjcwWrH62MrXzQDUjz6ClW04RKXSrBqxTqr"

def get_user_token():
    return "IBYFZYPmHugD0oxtGOwGt5pHj5Lc7rsmdN2FP9lP"

def get_glpi_host():

    return 'http://localhost:8081/'

def get_auth_token(url=get_glpi_host(), token=get_user_token() , app_token=get_api_token()):
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




def get_datas_problems():
    api_url = "https://systemframe.verdanadesk.com/apirest.php/Problem"
    session_token = get_auth_token() 
    headers = {
        'Session-Token': '9a30mi3emcl50es05jrfc83p08',
        'App-Token': 'UBhMtLCyfVAHfH40yNsCpD54z3OF2TUfeLCl5nyV'
    }
    problems = []
    offset = 0
    page = 1
    per_page = 50

    # Fazer a requisição GET para buscar todos os problemas
    while len(problems)<100:
        params = {
            'start':offset,
            'limit':per_page
        }
        response = requests.get(f"{api_url}?range=0-99999", headers=headers,params=params)

        if response.status_code == 200 or response.status_code == 206:
            data = response.json()
            if not data:
                break
            problems.extend(data)
            if len(data) < per_page:
                break
            page += 1
        else:
            print(f"Falha ao buscar problemas. Status Code: {response.status_code}")
            print("Detalhes do erro:", response.text)
            break

    return problems


def set_datas_problems():
    problems = get_datas_problems()
    session_token = get_auth_token() 
    headers = {
        'Session-Token': session_token,
        'App-Token': get_api_token()
    }
    for row in problems:
        glpi_data ={"input": {
            "name": row["name"],
            "content": row["content"],
            "status": row["status"],  # Exemplo: 2 = Em andamento
            "priority": row["priority"],  # Exemplo: 3 = Alta
            "date": row["date"],
            "date_mod": row["date_mod"]
        }}
        pass        
        logger.debug(f"Request: {json.dumps(glpi_data)}")
        try:
            response = requests.post(f'{get_glpi_host()}/apirest.php/Problem/', headers=headers, json=glpi_data)
            if response.status_code == 201:
                logger.debug(f'Problem created in GLPI: {response.json()}')
            else:
                logger.error("deu erro otario")
                logger.error(response.json())
        except Exception as e:
            pass
print(set_datas_problems())