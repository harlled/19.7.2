import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru/'

    def get_api_key(self, email: str, password: str) -> json:
        """Метод отправляет запрос к API сервера для получения уникального ключа пользователя
        по указанным email и паролю, и возвращает статус запроса и результат в формате json"""
        headers = {
            'email': email,
            'password': password
        }
        res = requests.get(self.base_url+'api/key', headers=headers)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def get_list_of_pets(self, auth_key: str, filter: str = "") -> json:
        """Метод отправляет запрос к API сервера для получения списка питомцев в соответствии с 
        указанным фильтром "my_pets" (для получения списка питомцев пользователя), или с 
        пустым фильтром (для отображения всех питомцев), имеющихся на сайте"""
        headers = {'auth_key': auth_key['key']}
        filter = {'filter': filter}
        res = requests.get(self.base_url+'api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_new_pet(self, auth_key: json, name: str, animal_type: str, age: str,
                    pet_photo: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце и его фото, и возвращает статус
        запроса на сервер, и результат в формате JSON с данными добавленного питомца"""
        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age,
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url+'api/pets', headers=headers, data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        print(result)
        return status, result

    def delete_pet(self, auth_key: json, pet_id: str) -> json:
        """Метод отправляет запрос на сервер для удаления существующего питомца по его ID,
        и возвращает статус запроса на сервер, и результат в формате json с информацией об удалении"""
        headers = {'auth_key': auth_key['key']}

        res = requests.delete(self.base_url+'/api/pets/'+pet_id, headers=headers)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        print(result)
        return status, result

    def update_pet_information(self, auth_key: json, pet_id: str, name: str, animal_type: str,
                               age: str) -> json:
        """Метод отправляет запрос на сервер для изменения информации о питомце по его ID и
        и возвращает статус запроса на сервер, и результат в формате json с информацией об изменениях"""
        headers = {'auth_key': auth_key['key']}
        data = {
                'name': name,
                'animal_type': animal_type,
                'age': age
        }
        res = requests.put(self.base_url+'api/pets/'+pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        return status, result

    def add_info_about_new_pet(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """Метод отправляет на сервер данные о добавляемом питомце и возвращает статус
        запроса на сервер, и результат в формате JSON с данными добавленного питомца"""
        data = {
                'name': name,
                'animal_type': animal_type,
                'age': age
        }
        headers = {'auth_key': auth_key['key']}

        res = requests.post(self.base_url+'/api/create_pet_simple', headers=headers, data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except:
            result = res.text
        print(result)
        return status, result

    def add_photo_to_pet(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """Метод отправляет на сервер фото к добавленному ранее ранее питомцу. Возвращает статус
        запроса  и данные питомца в JSON"""
        data = MultipartEncoder(
        fields={
            'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
        })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""

        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        return status, result




