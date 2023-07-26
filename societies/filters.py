from django_filters import rest_framework as filters

from societies.models import Society


class SocietyFilter(filters.FilterSet):
    rut = filters.CharFilter(field_name='rut__code')

    class Meta:
        model = Society
        fields = ["rut"]
