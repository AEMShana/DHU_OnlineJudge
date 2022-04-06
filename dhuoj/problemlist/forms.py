from django import forms
from .models import ProblemList

class ProblemListForm(forms.ModelForm):
    class Meta:
        model = ProblemList
        fields = ('listName', 'members')