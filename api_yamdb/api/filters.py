from django_filters.rest_framework import CharFilter, FilterSet, NumberFilter

from reviews.models import Title


class TitleFilters(FilterSet):
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')
    year = NumberFilter(field_name='year')
    name = CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
