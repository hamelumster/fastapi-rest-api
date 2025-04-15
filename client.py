import requests

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
create_adv = requests.post(
    "http://127.0.0.1:8000/api/v1/advertisement/",
    json={"title": "shoes",
          "description": "very good shoes",
          "price": 1000,
          "author": "user_4"}
)
print(create_adv.status_code)
print(create_adv.json())
