from django_filters import FilterSet, CharFilter, MultipleChoiceFilter, DateFromToRangeFilter, ModelChoiceFilter
from django import forms 
from announcement.models import Announcement, CATEGORY, Respond, RESPOND_STATUS, STATUS_CHOICES

class UserAnnouncementFilter(FilterSet):
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

    status = MultipleChoiceFilter(
        field_name='status',
        choices=STATUS_CHOICES,
        widget=forms.SelectMultiple,
        label='Status'
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
        fields = ['header', 'category', 'date', 'status']


class UserRespondFilter(FilterSet):
    text = CharFilter(
        field_name='text',
        lookup_expr='iregex',
        label='Text'
    )

    date = DateFromToRangeFilter(
        field_name='create_time',
        lookup_expr='gt',
        widget=forms.widgets.MultiWidget(
        widgets=[forms.DateInput(attrs={'type': 'date'}), forms.DateInput(attrs={'type': 'date'})]
        ),
        label='Date'
    )

    status = MultipleChoiceFilter(
        field_name='status',
        choices=RESPOND_STATUS,
        widget=forms.SelectMultiple,
        label='Status'
    )

    class Meta:
        model = Respond
        fields = ['text', 'date', 'status']

class IncomingRespondFilter(FilterSet):
    announcement = ModelChoiceFilter(
        field_name='announcement',
        queryset=Announcement.objects.none(), 
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Announcement'
    )

    text = CharFilter(
        field_name='text',
        lookup_expr='iregex',
        label='Text'
    )

    date = DateFromToRangeFilter(
        field_name='create_time',
        lookup_expr='gt',
        widget=forms.widgets.MultiWidget(
        widgets=[forms.DateInput(attrs={'type': 'date'}), forms.DateInput(attrs={'type': 'date'})]
        ),
        label='Date'
    )

    status = MultipleChoiceFilter(
        field_name='status',
        choices=RESPOND_STATUS,
        widget=forms.SelectMultiple,
        label='Status'
    )

    class Meta:
        model = Respond
        fields = ['text', 'date', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None) 
        super().__init__(*args, **kwargs)
        if user:
            self.filters['announcement'].queryset = Announcement.objects.filter(user=user)  