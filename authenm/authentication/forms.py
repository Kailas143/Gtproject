from django.contrib.auth.models import User
from django import forms 
from .models import User


class UserForm(forms.ModelForm):
    domain = forms.CharField(max_length=50)
    class Meta :
        model = User
        fields = ('username','password','domain',)
    