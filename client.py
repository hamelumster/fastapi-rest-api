import requests
from pprint import pprint


# Создание пользователя
# create_user = requests.post(
#     "http://127.0.0.1:8000/api/v1/user/",
#     json={"username": "Thomas", "password": "test_password"}
# )
# print(create_user.status_code)
# print(create_user.json())


# Получение пользователя
# get_user = requests.get("http://127.0.0.1:8000/api/v1/user/2")
# print(get_user.status_code)
# print(get_user.json())


# Создание объявления (в параметрах передается айди пользователя)
# create_adv = requests.post(
#     "http://127.0.0.1:8000/api/v1/advertisement/",
#     params={"user_id": 1},
#     json={"title": "boots",
#           "description": "very good boots, its true",
#           "price": 500
#           })
# print(create_adv.status_code)
# print(create_adv.json())


# Получение объявления
# get_adv = requests.get("http://127.0.0.1:8000/api/v1/advertisement/1")
# print(get_adv.status_code)
# pprint(get_adv.json())


# Обновление объявления
# update_adv = requests.patch(
#     "http://127.0.0.1:8000/api/v1/advertisement/1",
#     params={"user_id": 1},
#     json={"title": "laptop111111111",
#           "description": "good laptop new",
#           "price": 444444444
#           })
# print(update_adv.status_code)
# pprint(update_adv.json())


# Удаление объявления
# delete_adv = requests.delete("http://127.0.0.1:8000/api/v1/advertisement/1")
# print(delete_adv.status_code)
# pprint(delete_adv.json())


# Поиск объявления
# Раскомментировать параметры по необходимости
# search_adv = requests.get(
#     "http://127.0.0.1:8000/api/v1/advertisement",
#     params={# "title": "boots",
#             # "description": "very good boots, its true",
#             # "price": 500,
#             # "author": "Thomas"
#             })
# print(search_adv.status_code)
# pprint(search_adv.json())
