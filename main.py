import requests
import json

backend_url = "http://localhost:8000/"  # Ihre FastAPI-URL
login_data_su = {'username': 'tombenru', 'password': 'Marionetten'}
login_data_admin = {'username': 'tombom', 'password': '1234'}
login_data_actor = {'username': 'fali', 'password': 'fabian'}
new_admin_data = {'f_name': 'Thomas', 'l_name': 'Ruff', 'username': 'tombom', 'password': '1234'}
new_actor_data = {'f_name': 'Fabian', 'l_name': 'Link', 'artist_name': 'Bruno', 'username': 'fali', 'password': 'fabian'}

session = requests.Session()
response = session.post(f"{backend_url}token", login_data_actor)
response = json.loads(response.content.decode('utf-8'))
print(f'authorization-response: {response}')

# session.headers.update({"Authorization": 'Bearer ' + response['access_token']})
#
# response = session.post(f'{backend_url}admin/actor', json=new_actor_data)
#
# print(f'{response.json()=}')
