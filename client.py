import requests
from pprint import pprint


# Создание пользователя
# create_user = requests.post(
#     "http://127.0.0.1:8000/api/v1/user/",
#     json={"username": "user_4", "password": "test_password"}
# )
# print(create_user.status_code)
# print(create_user.json())


# Получение пользователя
# get_user = requests.get("http://127.0.0.1:8000/api/v1/user/100")
# print(get_user.status_code)
# print(get_user.json())


# Создание объявления
# create_adv = requests.post(
#     "http://127.0.0.1:8000/api/v1/advertisement/",
#     json={"title": "shoes",
#           "description": "very good shoes",
#           "price": 1000,
#           "author": "user_4"}
# )
# print(create_adv.status_code)
# print(create_adv.json())


# Получение объявления
# get_adv = requests.get("http://127.0.0.1:8000/api/v1/advertisement/10")
# print(get_adv.status_code)
# pprint(get_adv.json())


# Обновление объявления
# update_adv = requests.patch(
#     "http://127.0.0.1:8000/api/v1/advertisement/10",
#     json={"title": "shoes",
#           "description": "very good shoes, its true",
#           "price": 1111,
#           "author": "user_4"}
# )
# print(update_adv.status_code)
# pprint(update_adv.json())


# Удаление объявления
# delete_adv = requests.delete("http://127.0.0.1:8000/api/v1/advertisement/10")
# print(delete_adv.status_code)
# pprint(delete_adv.json())


# Поиск объявления
# Раскомментировать параметры по необходимости
search_adv = requests.get(
    "http://127.0.0.1:8000/api/v1/advertisement",
    params={# "title": "shoes",
            # "description": "very good shoes, its true",
            # "price": 1000,
            # "author": "user_4"
            })
print(search_adv.status_code)
pprint(search_adv.json())
