import json

import requests


backend_url = "http://localhost:8000/superuser/"

session = requests.Session()


new_su = {'f_name': 'Thomas', 'l_name': 'Ruff', 'username': 'tombenru', 'password': 'Marionetten'}

response = session.post(backend_url, json=new_su)

print(f'{response.json()}')

