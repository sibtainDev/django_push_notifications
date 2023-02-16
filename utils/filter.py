from pyexpat import model

from django.db.models.functions import Concat
from django_filters import FilterSet
from django_filters import rest_framework as filters
from django.db.models import Value as V
from django_filters.rest_framework import DjangoFilterBackend

from account.models import User, Employee


class MainFilter(DjangoFilterBackend):
    pass


def filter_by_name(queryset, value):
    return queryset.annotate(full_name=Concat('first_name', V(' '), 'last_name')).filter(
        full_name__icontains=value)


class EmployeeFilter(FilterSet):
    full_name = filters.CharFilter(method='full_name_filter', label='full_name')
    phone = filters.CharFilter(field_name='phone', label='phone', lookup_expr='icontains')
    user = filters.ModelChoiceFilter(field_name='user', queryset=User.objects.all())
    first_name = filters.CharFilter(field_name='first_name', label='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', label='last_name', lookup_expr='icontains')

    def full_name_filter(self,queryset, name, value):
        return filter_by_name(queryset, value)

    class Meta:
        model = Employee
        fields = ['full_name', 'first_name', 'last_name', 'phone', 'user']
