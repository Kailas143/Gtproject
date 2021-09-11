import json

import requests
from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .models import Dc_details


class UserPermission(permissions.BasePermission,generics.GenericAPIView):

    queryset=Dc_details.objects.all()
    parser_classes = [JSONParser]
    
        
    def get(self,request) :
            user=requests.get('http://127.0.0.1:8000/user/').json()
            user_list=[]
            for u in user :
                user_list.append(u)
                print(u)
          
            user_n=json.dumps(user)
            print(type(user_n))

            return Response(user)