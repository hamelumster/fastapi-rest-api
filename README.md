clone repo:

```bash
git clone git@github.com:hamelumster/fastapi-rest-api.git
```

to run locally:

1) pip install -r requirements.txt
2) tune DB connection
3) run "init_db.py"
4)  run "seed_roles.py"
5) run command: `uvicorn server:app`
6) open client.py to send some requests

for assign role admin to user (user_id) run this: ```python -m utils.assign_admin <user_id>```

for example: 
```python -m utils.assign_admin 1```


to run in docker:

0) ofc run docker desktop
1) docker-compose up (wait assembly db and app)
2) open client.py to send some requests
