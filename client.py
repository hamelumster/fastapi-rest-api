import requests
from pprint import pprint


# Создание пользователя
# create_user = requests.post(
#     "http://127.0.0.1:8000/api/v1/user/",
#     json={"username": "Thomas_admin", "password": "test_password"}
# )
# print(create_user.status_code)
# print(create_user.json())

# ------------------------------------------------------------------------------------- #

# Авторизация
# data = requests.post("http://127.0.0.1:8000/api/v1/login",
#                      json={"username": "Thomas_admin", "password": "test_password"})
# print(data.status_code)
# print(data.json())

# ------------------------------------------------------------------------------------- #

# Получение пользователя
# get_user = requests.get("http://127.0.0.1:8000/api/v1/user/3")
# print(get_user.status_code)
# print(get_user.json())

# ------------------------------------------------------------------------------------- #

# Обновление данных пользователя без токена
# patch_user = requests.patch("http://127.0.0.1:8000/api/v1/user/1",
#                             json={"username": "Jerry"})
# print(patch_user.status_code)
# print(patch_user.json())

# ------------------------------------------------------------------------------------- #

# Обновление данных пользователя с токеном
# header = {"x-token": "6a1275e8-c517-43bc-a854-e1d83ec7705d"}
# patch_user = requests.patch("http://127.0.0.1:8000/api/v1/user/1",
#                             headers=header,
#                             json={"username": "Jerry"})
# print(patch_user.status_code)
# print(patch_user.json())

# ------------------------------------------------------------------------------------- #

# Создание объявления без токена (в параметрах передается айди пользователя)
# create_adv = requests.post(
#     "http://127.0.0.1:8000/api/v1/advertisement/",
#     params={"user_id": 1},
#     json={"title": "boots",
#           "description": "very good boots, its true",
#           "price": 500
#           })
# print(create_adv.status_code)
# print(create_adv.json())

# ------------------------------------------------------------------------------------- #

# Создание объявления c токеном (в параметрах передается айди пользователя)
# header = {"x-token": "6a1275e8-c517-43bc-a854-e1d83ec7705d"}
# create_adv = requests.post(
#     "http://127.0.0.1:8000/api/v1/advertisement/",
#     headers=header,
#     json={"title": "boots",
#           "description": "very good boots, its true",
#           "price": 500
#           })
# print(create_adv.status_code)
# print(create_adv.json())

# ------------------------------------------------------------------------------------- #

# Получение объявления
# get_adv = requests.get("http://127.0.0.1:8000/api/v1/advertisement/1")
# print(get_adv.status_code)
# pprint(get_adv.json())

# ------------------------------------------------------------------------------------- #

# Обновление объявления без токена
# update_adv = requests.patch(
#     "http://127.0.0.1:8000/api/v1/advertisement/1",
#     params={"user_id": 1},
#     json={"title": "laptop111111111",
#           "description": "good laptop new",
#           "price": 444444444
#           })
# print(update_adv.status_code)
# pprint(update_adv.json())

# ------------------------------------------------------------------------------------- #

# Обновление объявления c токеном
# header = {"x-token": "6a1275e8-c517-43bc-a854-e1d83ec7705d"}
# update_adv = requests.patch(
#     "http://127.0.0.1:8000/api/v1/advertisement/1",
#     headers=header,
#     json={"title": "laptop111111111",
#           "description": "good laptop new",
#           "price": 444444444
#           })
# print(update_adv.status_code)
# pprint(update_adv.json())

# ------------------------------------------------------------------------------------- #

# Удаление объявления без токена
# delete_adv = requests.delete("http://127.0.0.1:8000/api/v1/advertisement/1")
# print(delete_adv.status_code)
# pprint(delete_adv.json())

# ------------------------------------------------------------------------------------- #

# Удаление объявления с токеном
# header = {"x-token": "6a1275e8-c517-43bc-a854-e1d83ec7705d"}
# delete_adv = requests.delete("http://127.0.0.1:8000/api/v1/advertisement/1",
#                              headers=header)
# print(delete_adv.status_code)
# pprint(delete_adv.json())

# ------------------------------------------------------------------------------------- #

# Поиск объявления
# Раскомментировать параметры по необходимости
# search_adv = requests.get(
#     "http://127.0.0.1:8000/api/v1/advertisement",
#     params={"title": "boots",
#             # "description": "very good boots, its true",
#             # "price": 500,
#             # "author": "Thomas"
#             })
# print(search_adv.status_code)
# pprint(search_adv.json())





# ------------------------- ADMIN REQUESTS -------------------------------------------- #

# Создание пользователя
# create_user = requests.post(
#     "http://127.0.0.1:8000/api/v1/user/",
#     json={"username": "Thomas_admin", "password": "test_password"}
# )
# print(create_user.status_code)
# print(create_user.json())

# ------------------------------------------------------------------------------------- #

# Авторизация
# data = requests.post("http://127.0.0.1:8000/api/v1/login",
#                      json={"username": "Thomas_admin", "password": "test_password"})
# print(data.status_code)
# print(data.json())

# ------------------------------------------------------------------------------------- #

# Изменение данных другого пользователя (админом)
# header = {"x-token": "33075b0d-c2c4-4653-b01f-30d85c8f38d4"}
# patch_user = requests.patch("http://127.0.0.1:8000/api/v1/user/1",
#                             headers=header,
#                             json={"username": "Jerry_admin_was_here"})
# print(patch_user.status_code)
# print(patch_user.json())

# ------------------------------------------------------------------------------------- #

# Изменение чужого объявления (админом)
# header = {"x-token": "6a1275e8-c517-43bc-a854-e1d83ec7705d"}
# update_adv = requests.patch(
#     "http://127.0.0.1:8000/api/v1/advertisement/1",
#     headers=header,
#     json={"title": "laptop111111111",
#           "description": "good laptop new",
#           "price": 444444444
#           })
# print(update_adv.status_code)
# pprint(update_adv.json())

# ------------------------------------------------------------------------------------- #

# Удаление пользователя (админом)
# header = {"x-token": "7beae5c1-ad63-4692-9ed3-b4c99a1f8da8"}
# delete_user = requests.delete("http://127.0.0.1:8000/api/v1/user/1",
#                              headers=header)
# print(delete_user.status_code)
# pprint(delete_user.json())