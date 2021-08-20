from django import forms
from . models import Users


class Subscribe(forms.ModelForm):
    class Meta :
        model = Users
        fields = '__all__'
    def __str__(self):
        return self.Email