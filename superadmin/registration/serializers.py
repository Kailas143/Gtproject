from rest_framework import serializers
from . models import Branding_Users

class Accepted_Serializers(serializers.ModelSerializer) :
    class Meta :
        model = Branding_Users
        fields='__all__'