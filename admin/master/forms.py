from django import forms

from .models import (Process, Processcost, Product, Productrequirements,
                     Productspec, Rawcomponent)


class ProcessForm(forms.ModelForm):
    
    class Meta:
        model = Process
        fields = "__all__"

class ProcesscostForm(forms.ModelForm):
    
    class Meta:
        model = Processcost
        fields = "__all__"

class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Product
        fields = "__all__"

class RawcomponentForm(forms.ModelForm):
    
    class Meta:
        model = Rawcomponent
        fields = "__all__"

class ProductrequirementsForm(forms.ModelForm):
    
    class Meta:
        model = Productrequirements
        fields = "__all__"

class ProductspecForm(forms.ModelForm):
    
    class Meta:
        model = Productspec
        fields = "__all__"
