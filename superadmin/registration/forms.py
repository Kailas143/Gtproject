from django import forms
from . models import Branding_Users

class Subscribe(forms.ModelForm):
    class Meta :
        model = Branding_Users
        fields = '__all__'
    def __str__(self):
        return self.Email