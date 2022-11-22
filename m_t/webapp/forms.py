from django import forms
from django.forms import widgets
from webapp.models import Todo
from django.core.validators import BaseValidator, ValidationError
from django.utils.deconstruct import deconstructible

# class TodoForm(forms.Form):
#     short_description = forms.CharField(label='short_description')
#     description = forms.CharField(label='description', widget=forms.Textarea())
#     status = forms.ModelChoiceField(queryset=Status.objects.all(), label='status', widget=widgets.Select)
#     type = forms.ModelMultipleChoiceField(required=False, label='type', queryset=Type.objects.all(), widget=forms.CheckboxSelectMultiple)

class TodoForm(forms.ModelForm):

    class Meta:
        model = Todo
        fields = ['short_description', 'description', 'status', 'type']
        # exclude = []
        widgets = {'type': widgets.CheckboxSelectMultiple}


    def clean_short_description(self):
        short_description = self.cleaned_data['short_description']
        if short_description.isdigit() == True:
            raise ValidationError('You entered only numbers, numbers only together with a string')

        return short_description

    def clean_description(self):
        description = self.cleaned_data['description']
        swear = ('nigger', 'shit', 'fuck', 'freak', 'bastard', 'hooker', 'poop')
        for s in swear:
            if s in description or s.capitalize() in description:
                raise ValidationError('There is a curse in your description')

        return description
