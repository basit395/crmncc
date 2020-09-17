import django_filters
from .models import nazeel

class nazeelFilter(django_filters.FilterSet):

    nazeelname = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = nazeel
        fields = ['nazeelname','jail']
