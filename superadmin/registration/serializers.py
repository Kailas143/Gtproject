from rest_framework import serializers

from .models import Registered_users


class Accepted_Serializers(serializers.ModelSerializer) :
    class Meta :
        model = Registered_users
        fields='__all__'