import requests
import json

backend_url = "http://localhost:8000/"  # Ihre FastAPI-URL
login_data = {'username': 'tombenru', 'password': 'Marionetten'}
new_admin_data = {'f_name': 'Thomas', 'l_name': 'Ruff', 'username': 'tombom', 'password': '1234'}

session = requests.Session()
response = session.post(f"{backend_url}token", login_data)
response = json.loads(response.content.decode('utf-8'))
print(f'authorization-response: {response}')

session.headers.update({"Authorization": 'Bearer ' + response['access_token']})

response = session.post(f'{backend_url}superuser/admin', json=new_admin_data)

print(f'{response.json()=}')
