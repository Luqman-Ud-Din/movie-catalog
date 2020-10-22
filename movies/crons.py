from datetime import datetime

from movie_catalog.services.ghibliapi import fetch_movies_with_people
from movies.models import Movie, Person, MoviePerson


def populate_movies():
    print(f'populate_movies started at: {datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}')

    for _movie in fetch_movies_with_people():
        if _movie.get('film') is None:
            continue

        movie, __ = Movie.objects.get_or_create(
            movie_id=_movie['film']['id'],
            defaults={
                'title': _movie['film']['title'],
                'description': _movie['film']['description'],
                'producer': _movie['film']['producer'],
                'director': _movie['film']['director'],
                'release_date': _movie['film']['release_date'],
                'rt_score': _movie['film']['rt_score'],
            }
        )

        for _person in _movie.get('people') or []:
            person, __ = Person.objects.get_or_create(
                member_id=_person['id'],
                defaults={
                    'name': _person['name']
                }
            )

            MoviePerson.objects.get_or_create(movie=movie, person=person)
