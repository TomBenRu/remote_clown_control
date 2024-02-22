import requests
import json

backend_url = "http://localhost:8000/"  # Ihre FastAPI-URL
endpoints = {'superuser': 'superuser/',
             'create_institution': 'superuser/institution-actors/',
             'create_location': 'admin/location/',
             'create_department': 'admin/department/',
             'create_actor': 'admin/actor/'}

login_data_su = {'username': 'tombenru', 'password': 'Marionetten'}
login_data_admin_institution_actors = {'username': 'tombom', 'password': '1234'}
login_data_admin_location_1 = {'username': 'sylvi', 'password': 'sylvi1234'}
login_data_admin_location_2 = {'username': 'bea', 'password': 'bea1234'}
login_data_admin_location_3 = {'username': 'kari', 'password': 'kari1234'}
login_data_actor = {'username': 'fali', 'password': 'fabian'}

new_admin_institution_actors__data = {'f_name': 'Thomas', 'l_name': 'Ruff', 'username': 'tombom', 'password': '1234'}
new_institution_actors_data = {'name': 'Humor Hilft Heilen'}

new_admin_location_data_1 = {'f_name': 'Sylvia', 'l_name': 'Becker', 'username': 'sylvi', 'password': 'sylvi1234'}
new_admin_location_data_2 = {'f_name': 'Beate', 'l_name': 'Blum', 'username': 'bea', 'password': 'bea1234'}
new_admin_location_data_3 = {'f_name': 'Karin', 'l_name': 'Kling', 'username': 'kari', 'password': 'kari1234'}
new_location_data_1 = {'name': 'Diakonissen Speyer', 'institution_actors_id': '2cb1a781-109e-4319-87e5-136e74af9a40'}
new_location_data_2 = {'name': 'SRH Langensteinbach', 'institution_actors_id': '2cb1a781-109e-4319-87e5-136e74af9a40'}
new_location_data_3 = {'name': 'Kinderklinik Schömberg', 'institution_actors_id': '2cb1a781-109e-4319-87e5-136e74af9a40'}

new_actor_data_1 = {'f_name': 'Fabian', 'l_name': 'Link', 'artist_name': 'Bruno', 'username': 'fali',
                    'password': 'fabian', 'institution_actors_id': '2cb1a781-109e-4319-87e5-136e74af9a40'}
new_actor_data_2 = {'f_name': 'Berenike', 'l_name': 'Felger', 'artist_name': 'Kamilla', 'username': 'bere',
                    'password': 'bere123', 'institution_actors_id': '2cb1a781-109e-4319-87e5-136e74af9a40'}
new_actor_data_3 = {'f_name': 'Thomas', 'l_name': 'Ruff', 'artist_name': 'Karotte', 'username': 'tom',
                    'password': 'tom123', 'institution_actors_id': '2cb1a781-109e-4319-87e5-136e74af9a40'}

new_department_data_1_1 = {'username': 'station_2b', 'password': 's2b', 'name': 'Station 2b',
                           'descriptive_name': 'Kinderstation', 'location_id': '27e19827-c252-49a1-b127-2a4847df7492'}
new_department_data_1_2 = {'username': 'station_5a', 'password': 's5a', 'name': 'Station 5a',
                           'descriptive_name': 'Gefäßchirurgie', 'location_id': '27e19827-c252-49a1-b127-2a4847df7492'}
new_department_data_2_1 = {'username': 'srh_karlsruhe', 'password': 'srh_karl', 'name': 'Station Karlsruhe',
                           'descriptive_name': 'Orthopädie', 'location_id': '0f306739-09ff-434c-995f-95c406f91318'}
new_department_data_3_1 = {'username': 'kiki_schöm_a', 'password': 'schöm_a', 'name': 'Station A',
                           'descriptive_name': 'Kinderstation', 'location_id': '6550c3a7-f79c-42a8-bf0c-eb8dda3f1960'}
new_department_data_3_2 = {'username': 'kiki_schöm_b', 'password': 'schöm_b', 'name': 'Station B',
                           'descriptive_name': 'Kinderstation', 'location_id': '6550c3a7-f79c-42a8-bf0c-eb8dda3f1960'}
new_department_data_3_3 = {'username': 'kiki_schöm_c', 'password': 'schöm_c', 'name': 'Station C',
                           'descriptive_name': 'Kinderstation', 'location_id': '6550c3a7-f79c-42a8-bf0c-eb8dda3f1960'}
new_department_data_3_4 = {'username': 'kiki_schöm_d', 'password': 'schöm_d', 'name': 'Station D',
                           'descriptive_name': 'Kinderstation', 'location_id': '6550c3a7-f79c-42a8-bf0c-eb8dda3f1960'}


def create_superuser():
    response = requests.post(f"{backend_url}superuser",
                             json={'f_name': 'Thomas', 'l_name': 'Ruff', 'username': 'tombenru', 'password': 'Marionetten'})
    print(f'{response.status_code=}')
    print(f'{response.json()=}')


# create_superuser()


def other_requests(endpoint: str, login_data: dict, new_data_1: dict, new_data_2: dict = None):
    session = requests.Session()
    response = session.post(f"{backend_url}token", login_data)
    if (status_code := response.status_code) != 200:
        print(f'{status_code=}')
        return
    response = json.loads(response.content.decode('utf-8'))

    print(f'authorization-response: {response}')

    session.headers.update({"Authorization": 'Bearer ' + response['access_token']})

    if new_data_2:
        response = session.post(f'{backend_url}{endpoint}', json={'user': new_data_1,
                                                                  'location': new_data_2})
    else:
        response = session.post(f'{backend_url}{endpoint}', json=new_data_1)

    print(f'{response.status_code=}')
    print(f'{response.json()=}')


# create_superuser()
other_requests(endpoints['create_actor'], login_data_admin_institution_actors,
               new_actor_data_3)
