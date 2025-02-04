from django import forms
from tinymce.widgets import TinyMCE
from .models import Announcement, CATEGORY, Respond

class AnnouncementForm(forms.ModelForm):
    header = forms.CharField(
        label='Название объявления',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    content = forms.CharField(
        label='Содержимое',
        widget=TinyMCE(attrs={'cols': 80, 'rows': 30})
    )
    category = forms.ChoiceField(
        label='Тип',
        choices=CATEGORY,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )

    class Meta:
        model = Announcement
        fields = ['header', 'content', 'category']


class RespondForm(forms.ModelForm):
    class Meta:
        model = Respond
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control'}),
        }
