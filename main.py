import requests
import json

backend_url = "http://localhost:8000/"  # Ihre FastAPI-URL
login_data_su = {'username': 'tombenru', 'password': 'Marionetten'}
login_data_admin_institution_actors = {'username': 'tombom', 'password': '1234'}
login_data_admin_location_1 = {'username': 'sylvi', 'password': 'sylvi1234'}
login_data_admin_location_2 = {'username': 'bea', 'password': 'bea1234'}
login_data_actor = {'username': 'fali', 'password': 'fabian'}
new_admin_institution_actors__data = {'f_name': 'Thomas', 'l_name': 'Ruff', 'username': 'tombom', 'password': '1234'}
new_institution_actors_data = {'name': 'Humor Hilft Heilen'}
new_admin_location_data_1 = {'f_name': 'Sylvia', 'l_name': 'Becker', 'username': 'sylvi', 'password': 'sylvi1234'}
new_admin_location_data_2 = {'f_name': 'Beate', 'l_name': 'Blum', 'username': 'bea', 'password': 'bea1234'}
new_location_data_1 = {'name': 'Diakonissen Speyer', 'institution_actors_id': '87D4B64417644BB1B0B818C66EBFA6D8'}
new_location_data_2 = {'name': 'SRH Langensteinbach', 'institution_actors_id': '87D4B64417644BB1B0B818C66EBFA6D8'}
new_actor_data_1 = {'f_name': 'Fabian', 'l_name': 'Link', 'artist_name': 'Bruno', 'username': 'fali',
                    'password': 'fabian', 'institution_actors_id': '87D4B64417644BB1B0B818C66EBFA6D8'}
new_actor_data_2 = {'f_name': 'Berenike', 'l_name': 'Felger', 'artist_name': 'Kamilla', 'username': 'bere',
                    'password': 'bere123', 'institution_actors_id': '87D4B64417644BB1B0B818C66EBFA6D8'}
new_department_data_1_1 = {'username': 'station_2b', 'password': 's2b', 'name': 'Station 2b',
                           'descriptive_name': 'Kinderstation', 'location_id': 'AA0B68C3741447FF9BE2ADF71EF0822D'}
new_department_data_1_2 = {'username': 'station_5a', 'password': 's5a', 'name': 'Station 5a',
                           'descriptive_name': 'Gefäßchirurgie', 'location_id': 'AA0B68C3741447FF9BE2ADF71EF0822D'}


def create_superuser():
    response = requests.post(f"{backend_url}superuser",
                             json={'f_name': 'Thomas', 'l_name': 'Ruff', 'username': 'tombenru', 'password': 'Marionetten'})
    print(f'{response.status_code=}')
    print(f'{response.json()=}')


# create_superuser()


def other_requests():
    session = requests.Session()
    response = session.post(f"{backend_url}token", login_data_admin_location_1)
    if (status_code := response.status_code) != 200:
        print(f'{status_code=}')
        return
    response = json.loads(response.content.decode('utf-8'))

    print(f'authorization-response: {response}')

    session.headers.update({"Authorization": 'Bearer ' + response['access_token']})

    response = session.post(f'{backend_url}admin/department',
                            json=new_department_data_1_2)

    print(f'{response.json()=}')


other_requests()
