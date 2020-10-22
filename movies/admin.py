from django.contrib import admin

from movies.models import Movie, Person, MoviePerson

admin.site.register(Movie)
admin.site.register(Person)
admin.site.register(MoviePerson)
