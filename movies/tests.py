import json
from unittest.mock import patch

import requests
from django.test import TestCase
from django.urls import reverse

from movie_catalog.services.ghibliapi import FILM_URL, PEOPLE_URL, fetch_movies_with_people
from movies.crons import populate_movies
from movies.models import Movie, Person

MOVIE_1 = {
    "id": "2baf70d1-42bb-4437-b551-e5fed5a87abe",
    "title": "Castle in the Sky",
    "description": "test description",
    "director": "Hayao Miyazaki",
    "producer": "Isao Takahata",
    "release_date": "1986",
    "rt_score": "95"
}

MOVIE_2 = {
    "id": "12cfb892-aac0-4c5b-94af-521852e46d6a",
    "title": "Grave of the Fireflies",
    "description": "test description",
    "director": "Isao Takahata",
    "producer": "Toru Hara",
    "release_date": "1988",
    "rt_score": "97"
}

PERSON_1 = {
    "id": "ba924631-068e-4436-b6de-f3283fa848f0",
    "name": "Ashitaka",
    "gender": "male",
    "age": "late teens",
    "eye_color": "brown",
    "hair_color": "brown",
    "films": [
        "https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe"
    ],
    "species": "https://ghibliapi.herokuapp.com/species/af3910a6-429f-4c74-9ad5-dfe1c4aa04f2",
    "url": "https://ghibliapi.herokuapp.com/people/ba924631-068e-4436-b6de-f3283fa848f0"
}

PERSON_2 = {
    "id": "030555b3-4c92-4fce-93fb-e70c3ae3df8b",
    "name": "Yakul",
    "age": "Unknown",
    "gender": "male",
    "eye_color": "Grey",
    "hair_color": "Brown",
    "films": [
        "https://ghibliapi.herokuapp.com/films/12cfb892-aac0-4c5b-94af-521852e46d6a"
    ],
    "species": "https://ghibliapi.herokuapp.com/species/6bc92fdd-b0f4-4286-ad71-1f99fb4a0d1e",
    "url": "https://ghibliapi.herokuapp.com/people/030555b3-4c92-4fce-93fb-e70c3ae3df8b"
}

MOVIES_WITH_PEOPLE = [
    {
        "film": {
            "id": "2baf70d1-42bb-4437-b551-e5fed5a87abe",
            "title": "Castle in the Sky",
            "description": "test description",
            "director": "Hayao Miyazaki",
            "producer": "Isao Takahata",
            "release_date": "1986",
            "rt_score": "95"
        },
        "people": [
            {
                "id": "ba924631-068e-4436-b6de-f3283fa848f0",
                "name": "Ashitaka",
                "gender": "male",
                "age": "late teens",
                "eye_color": "brown",
                "hair_color": "brown",
                "films": [
                    "https://ghibliapi.herokuapp.com/films/2baf70d1-42bb-4437-b551-e5fed5a87abe"
                ],
                "species": "https://ghibliapi.herokuapp.com/species/af3910a6-429f-4c74-9ad5-dfe1c4aa04f2",
                "url": "https://ghibliapi.herokuapp.com/people/ba924631-068e-4436-b6de-f3283fa848f0"
            }
        ]
    },
    {
        "film": {
            "id": "12cfb892-aac0-4c5b-94af-521852e46d6a",
            "title": "Grave of the Fireflies",
            "description": "test description",
            "director": "Isao Takahata",
            "producer": "Toru Hara",
            "release_date": "1988",
            "rt_score": "97"
        },
        "people": [
            {
                "id": "030555b3-4c92-4fce-93fb-e70c3ae3df8b",
                "name": "Yakul",
                "age": "Unknown",
                "gender": "male",
                "eye_color": "Grey",
                "hair_color": "Brown",
                "films": [
                    "https://ghibliapi.herokuapp.com/films/12cfb892-aac0-4c5b-94af-521852e46d6a"
                ],
                "species": "https://ghibliapi.herokuapp.com/species/6bc92fdd-b0f4-4286-ad71-1f99fb4a0d1e",
                "url": "https://ghibliapi.herokuapp.com/people/030555b3-4c92-4fce-93fb-e70c3ae3df8b"
            }
        ]
    }
]

MOVIES = [MOVIE_1, MOVIE_2]
PEOPLE = [PERSON_1, PERSON_2]


def mock_get_request(url):
    response = requests.Response()
    response.status_code = 200

    if url == FILM_URL:
        response._content = json.dumps(MOVIES).encode()

    if url == PEOPLE_URL:
        response._content = json.dumps(PEOPLE).encode()

    return response


class MovieListTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super(MovieListTestCase, cls).setUpClass()

        with patch('movies.crons.fetch_movies_with_people', return_value=MOVIES_WITH_PEOPLE):
            populate_movies()

    def test_fetch_movies_with_people(self):
        with patch('requests.get', side_effect=mock_get_request):
            movies_with_people = fetch_movies_with_people()

        self.assertEqual(movies_with_people, MOVIES_WITH_PEOPLE)

    def test_populate_movies_and_people(self):
        self.assertEqual(Movie.objects.count(), len(MOVIES))
        self.assertEqual(Person.objects.count(), len(PEOPLE))

    def test_movie_list_view(self):
        url = reverse('movies-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
