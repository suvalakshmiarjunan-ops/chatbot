from django import forms
from .models import User

class TaggingForm(forms.Form):
    tag_name = forms.CharField(label='Tag Name', max_length=100)
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Select Users'
    )
