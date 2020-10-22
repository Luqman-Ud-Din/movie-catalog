from django.views.generic import ListView

from movies.models import Movie


class MoviesListView(ListView):
    template_name = 'movies_list.html'
    context_object_name = 'movies'
    queryset = Movie.objects.order_by('-release_date')
