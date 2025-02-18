from django import forms

from todoapp.models import TodoModel


class TodoForm(forms.ModelForm):
    class Meta:
        model = TodoModel
        fields = ["title"]
