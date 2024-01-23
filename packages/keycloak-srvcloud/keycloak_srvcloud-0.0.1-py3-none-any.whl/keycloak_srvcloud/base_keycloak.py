import requests

class Keycloak:
    '''Класс для работы с keycloak'''
    keycloak_host = ""
    keycloak_port = ""
    client_id = ""
    client_secret = ""
    api_url = ""

    def __init__(self, keycloak_host, keycloak_port, realm_name,
                 client_id, client_secret) -> None:
        self.keycloak_host = keycloak_host
        self.keycloak_port = keycloak_port
        self.realm_name = realm_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.api_url = f'http://{keycloak_host}:{keycloak_port}/realms/{realm_name}/protocol/openid-connect'

    def auth(self, username: str, password: str) -> dict:
        '''Авторизация в keycloak'''
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': username,
            'password': password,
            'grant_type': "password"
        }
        response = requests.post(f'{self.api_url}/token', data=data, timeout=3)
        response.raise_for_status()
        return response.json()

    def refresh_token(self, access_token: str, refresh_token: str) -> dict:
        '''Обновление токена'''
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'accesss_token': access_token,
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }
        response = requests.post(f'{self.api_url}/token', data=data, timeout=3)
        response.raise_for_status()
        return response.json()


    def logout(self, access_token: str, refresh_token: str) -> None:
        '''Завершает сессию'''
        headers = {
            'Authorization': f"Bearer {access_token}",
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': refresh_token
        }
        response = requests.post(f'{self.api_url}/logout', data=data, headers=headers, timeout=3)
        response.raise_for_status()


    def revoke(self, access_token: str) -> None:
        '''Отозвать токен'''
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'token': access_token,
            'token_type_hint': 'access_token'
        }
        response = requests.post(f'{self.api_url}/revoke', data=data, timeout=3)
        response.raise_for_status()


    def userinfo(self, access_token: str) -> dict:
        '''Получение userinfo'''
        headers = {
            'Authorization': f"Bearer {access_token}",
            'Content-Type': 'application/json'
        }
        response = requests.get(f'{self.api_url}/userinfo', headers=headers, timeout=3)
        response.raise_for_status()
        return response.json()


    def introspect(self, access_token: str) -> dict:
        '''Получение интроспекции токена'''
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'token': access_token
        }
        response = requests.post(f'{self.api_url}/token/introspect', data=data, timeout=3)
        response.raise_for_status()
        return response.json()
