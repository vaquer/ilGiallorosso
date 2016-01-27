import autocomplete_light
from django import forms
from .models import Entry


class EntryFormAutocomplete(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['title', 'about', 'text', 'photo', 'active', 'top', 'author', 'category', 'tags']
        widgets = {
            'tags': autocomplete_light.MultipleChoiceWidget('TagAutocomplete', attrs={
                'data-autocomplete-minimum-characters': 1,
                'placeholder': 'Selecciona los tags ...',
                'class': 'multiplechoicewidget'},
                widget_attrs={'data-widget-maximum-values': 10}),
        }
