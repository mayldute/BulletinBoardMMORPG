from django_filters import FilterSet, CharFilter, MultipleChoiceFilter, DateFromToRangeFilter
from django import forms 
from .models import Announcement, CATEGORY

class AnnouncementFilter(FilterSet):
    header = CharFilter(
        field_name='header',
        lookup_expr='iregex',
        label='Header'
    )

    category = MultipleChoiceFilter(
        field_name='category',
        choices=CATEGORY,
        widget=forms.SelectMultiple,
        label='Category'
    )

    date = DateFromToRangeFilter(
        field_name='create_time',
        lookup_expr='gt',
        widget=forms.widgets.MultiWidget(
        widgets=[forms.DateInput(attrs={'type': 'date'}), forms.DateInput(attrs={'type': 'date'})]
        ),
        label='Date'
    )

    class Meta:
        model = Announcement
        fields = ['header', 'category', 'date']
        

