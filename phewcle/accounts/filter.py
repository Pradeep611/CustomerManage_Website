import django_filters
from .models import *
from django_filters import DateFilter
from django import forms

class FilterForm(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created',
                                           widget= forms.DateInput(attrs={'type': 'date'}),
                                           lookup_expr='gte', label='Start Date')

    end_date = DateFilter(field_name='date_created',
                                         widget= forms.DateInput(attrs={ 'type': 'date'}),
                                         lookup_expr='lte', label='End Date')
    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer','date_created']
        