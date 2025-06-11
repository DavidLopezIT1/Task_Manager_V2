# from django.forms import ModelForm
# from .models import Task

# class TaskForm(ModelForm):
#     class Meta:
#         model = Task
#         fields = ['title', 'description', 'important']

# En tu archivo forms.py

from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important', 'status', 'imagen']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Título de la tarea'}),
            'description': forms.Textarea(attrs={'placeholder': 'Descripción de la tarea', 'rows': 4}),
            'status': forms.Select(choices=[
                ('pendiente', 'Pendiente'),
                ('en_proceso', 'En Proceso'),
                ('completada', 'Completada'),
            ]),
            'important': forms.CheckboxInput(),
            'imagen': forms.FileInput(attrs={'accept': 'image/*'}),
        }

