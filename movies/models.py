from django.db import models


class Movie(models.Model):
    movie_id = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=256)
    description = models.TextField(default='')
    director = models.CharField(max_length=256)
    producer = models.CharField(max_length=256)
    release_date = models.IntegerField()
    rt_score = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.movie_id} / {self.title}'


class Person(models.Model):
    member_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.member_id} / {self.name}'


class MoviePerson(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_person')
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='movie_person')

    def __str__(self):
        return f'{self.movie.title} / {self.person.name}'

    class Meta:
        unique_together = [('movie', 'person',)]
