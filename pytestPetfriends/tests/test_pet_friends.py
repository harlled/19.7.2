from api import PetFriends
from settings import valid_email, valid_password
from settings import invalid_email, invalid_password
pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """Проверяем, что запрос API ключа возвращает статус 200, и в результате содержится 'key'"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_all_pets_with_valid_key(filter=''):
    """Проверяем, что запрос списка питомцев возвращает не пустой список"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name="Maxus", animal_type='cat', age='3', pet_photo='images/scottish-fold.jpg'):
    """Проверяем, можно ли добавить питомца с корректными данными"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_pet():
    """Проверяем, возможно ли удалить питомца"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Проверяем - если список своих питомцев пустой, то добавляем
    # нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, 'Макс', 'кот', '8', 'images/max.jpg')
        _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    assert status == 200
    assert pet_id not in my_pets.values()

def test_update_pet_info(name="Barsik", animal_type='cat', age='2'):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_information(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_add_info_about_new_pet(name="Barsik", animal_type='cat', age='2'):
    """Проверяем возможность добавления корректной информации о новом питомце без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_info_about_new_pet(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_add_photo_to_pet(pet_photo='images/max.jpg'):
    """Проверяем возможно ли добавить фото питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_to_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем что статус ответа = 200 и фото питомца соответствует заданному
        assert status == 200
        assert 'image' in result['pet_photo']
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#1
def test_get_my_pets_with_valid_key(filter='my_pets'):
    """Проверяем, что запрос списка питомцев пользователя возвращает не пустой список"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

#2
def test_add_new_pet_with_invalid_data(name="", animal_type='', age='', pet_photo='images/scottish-fold.jpg'):
    """Проверяем, что запрос к серверу на добавление питомца с пустыми полями ввода
    возвращает статус 400"""
    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Баг!!! Приложение не должно принимать пустые поля для обязательных полей ввода.
    # Поэтому ожидаем ответ от сервера с кодом 200 вместо 400.
    assert status == 200
    assert result['name'] == name

#3
def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
    """Проверяем, что запрос API ключа с некорректным email возвращает статус 403,
    и в результате не содержится 'key'"""
    status, result = pf.get_api_key_incorrect(email, password)
    # Ожидаем ответ от сервера с кодом 403
    assert status == 403
    assert 'key' not in result

#4
def test_get_api_key_for_invalid_user_password(email=valid_email, password=invalid_password):
    """Проверяем, что запрос API ключа с некорректным паролем возвращает статус 403,
    и в результате не содержится 'key'"""
    status, result = pf.get_api_key(email, password)
    # Ожидаем ответ от сервера с кодом 403
    assert status == 403
    assert 'key' not in result

#5
def test_update_empty_pet_info(name='!"№', animal_type='34', age='старый'):
    """Проверяем возможность обновления некорректной информации о питомце"""
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_information(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Баг!!! Приложение не должно принимать буквенные значения в поле ввода 'age',
        # цифровые значения в поле "animal_type", символы в поле ввода "name".
        # Поэтому ожидаем ответ от сервера с кодом 200 вместо 400.
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#6
def test_add_empty_info_about_new_pet(name="", animal_type='', age=''):
    """Проверяем, что приложение не дает отправить запрос на добавление информации
    о питомце с путыми полями ввода"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_info_about_new_pet(auth_key, name, animal_type, age)
    # Баг!!! Приложение не должно принимать пустые поля для обязательных полей ввода.
    # Поэтому ожидаем ответ от сервера с кодом 200 вместо 400.
    assert status == 200

#7
def test_add_incorrect_photo_to_pet(pet_photo='images/123.png'):
    """Проверяем, что запрос к серверу с некорректным форматом
     прикрепленного изображения возвращает статус 500"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')
    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_to_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем что статус ответа = 500
        assert status == 500
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

#8
def test_add_long_name_to_new_pet(name="Bjdfd23273Пролавраорыартчпмлдоо8759489568348!2»%№№?№*((№)№_№-$%&"
                                       "&&(*()*)_{l,.//,.0≤°αjdfd23273Пролавраорыартчпмлдоо8759489568348!2"
                                       "»%№№?№*((№)№_№-%&&&(*()*)_{l,.//,.0≤°jdfd23273Пролавраорыартчпмлдоо"
                                       "8759489568348!2»%№№?№*((№)№_№-$%&&&(*()*)_{l,.//,.0≤°d2224dg57",
                                  animal_type='cat', age='<script>alert("Поле уязвимо!")</script>'):
    """Проверяем, что запрос к серверу c длинным именем возвращает статус 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_info_about_new_pet(auth_key, name, animal_type, age)
    # Баг!!! Приложение не должно принимать длинные значения для обязательных полей ввода.
    # Поэтому ожидаем ответ от сервера с кодом 200 вместо 400.
    assert status == 200
    assert result['name'] == name

#9
def test_add_XSS_name_to_new_pet(name='<script>alert("Поле уязвимо!")</script>',
                                  animal_type='cat', age='2'):
    """Проверяем, что запрос к серверу с XSS инъекцией в поле ввода 'name' возвращает статус 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_info_about_new_pet(auth_key, name, animal_type, age)
    # Баг!!! Приложение не должно принимать XSS инъекции для обязательных полей ввода.
    # Поэтому ожидаем ответ от сервера с кодом 200 вместо 400.
    assert status == 200

#10
def test_add_letter_symb_to_new_pet_age(name='Murzik',
                                  animal_type='cat', age='old'):
    """Проверяем, что запрос к серверу с буквенным значением в поле ввода 'age' возвращает статус 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_info_about_new_pet(auth_key, name, animal_type, age)
    # Баг!!! Приложение не должно принимать буквенные значения в поле ввода 'age'.
    # Поэтому ожидаем ответ от сервера с кодом 200 вместо 400.
    assert status == 200














