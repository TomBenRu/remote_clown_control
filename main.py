import requests
import json

backend_url = "http://localhost:8000/"  # Ihre FastAPI-URL
login_data_su = {'username': 'tombenru', 'password': 'Marionetten'}
login_data_admin_institution_actors = {'username': 'tombom', 'password': '1234'}
login_data_admin_location = {'username': 'sylvi', 'password': 'sylvi1234'}
login_data_actor = {'username': 'fali', 'password': 'fabian'}
new_admin_institution_actors__data = {'f_name': 'Thomas', 'l_name': 'Ruff', 'username': 'tombom', 'password': '1234'}
new_institution_actors_data = {'name': 'Humor Hilft Heilen'}
new_admin_location_data = {'f_name': 'Sylvia', 'l_name': 'Becker', 'username': 'sylvi', 'password': 'sylvi1234'}
new_location_data = {'name': 'Diakonissen Speyer'}
new_actor_data = {'f_name': 'Fabian', 'l_name': 'Link', 'artist_name': 'Bruno', 'username': 'fali',
                  'password': 'fabian', 'institution_actors_id': 'D5C2B20B38D343AB9F7950E53FB7F13F'}
new_department_data = {'username': 'station_2b', 'password': 's2b', 'name': 'Station 2b',
                       'descriptive_name': 'Kinderstation', 'location_id': '7B81CEA1FFC04E7086DD47AD69F62D8C'}


def create_superuser():
    response = requests.post(f"{backend_url}superuser",
                             json={'f_name': 'Thomas', 'l_name': 'Ruff', 'username': 'tombenru', 'password': 'Marionetten'})
    print(f'{response.status_code=}')
    print(f'{response.json()=}')


# create_superuser()


def other_requests():
    session = requests.Session()
    response = session.post(f"{backend_url}token", login_data_admin_location)
    if (status_code := response.status_code) != 200:
        print(f'{status_code=}')
        return
    response = json.loads(response.content.decode('utf-8'))

    print(f'authorization-response: {response}')

    session.headers.update({"Authorization": 'Bearer ' + response['access_token']})

    response = session.post(f'{backend_url}admin/department', json=new_department_data)

    print(f'{response.json()=}')


other_requests()
