import requests

BASE_URL = 'https://ghibliapi.herokuapp.com'
RESPONSE_LIMIT = 250

FILM_FIELDS = ['id', 'title', 'description', 'director', 'producer', 'release_date', 'rt_score']
FILM_URL = f'{BASE_URL}/films?fields={",".join(FILM_FIELDS)}&limit={RESPONSE_LIMIT}'

PEOPLE_FIELDS = ['id', 'name', 'films']
PEOPLE_URL = f'{BASE_URL}/people?fields={",".join(PEOPLE_FIELDS)}&limit={RESPONSE_LIMIT}'


def fetch_movies_with_people():
    films_response = requests.get(FILM_URL)
    people_response = requests.get(PEOPLE_URL)

    film_people_map = {film['id']: {'film': film} for film in films_response.json()}

    for person in people_response.json():
        for film in person['films']:
            film_id = film.split('/')[-1]

            if film_people_map.get(film_id) is None:
                film_people_map[film_id] = {}

            if film_people_map[film_id].get('people') is None:
                film_people_map[film_id]['people'] = []

            film_people_map[film_id]['people'].append(person)

    return list(film_people_map.values())
