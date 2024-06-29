import requests
from config import URL

class PetFriends:
    def __init__(self):
        self.base_url = URL

    def get_api_key(self, email, password):
        """ GET запрос получения api_key"""
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url + 'api/key', headers = headers)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key, filter):
        """ Получение списка всех питомцев, если 'filter' не задан,
        и только своих, если 'filter'='my_pets' """
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ''
        try:
            result = res.json()
        except:
            result = res.text
        return status, result