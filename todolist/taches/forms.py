from django.contrib.auth.forms import UserCreationForm
from .models import CustomerUser
from django import forms
from .models import Task

class UseregistrationForm(UserCreationForm):
    class Meta:
        model = CustomerUser
        fields = ('email', 'password1', 'password2', 'age' , 'Telephone' , 'Pays' , 'ville' , 'cond_ut')



class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'completed', 'category']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }




class ImportTasksForm(forms.Form):
    csv_file = forms.FileField()

