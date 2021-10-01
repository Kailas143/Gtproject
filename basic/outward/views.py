
from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from dispatch.models import Dispatch_details, Dispatch_materials

from .models import outward_details, outward_materials
from .serializers import outward_materials_serializers, outward_serializers


# Create your views here.
class Outward_API(generics.GenericAPIView,APIView,mixins.ListModelMixin):
    serializer_class = outward_serializers
    queryset=outward_details.objects.all()

    def get(self,request) :
        return self.list(request)
    
    def post(self,request) :
        outward_details_r=request.data[0]
        outward_materials_r=request.data[1]
        print(outward_details_r)
        print(outward_materials_r)
        serializer = outward_serializers(data=outward_details_r)
        if serializer.is_valid():
            outward_r=serializer.save()
            print(outward_r.vehicle_number)
            
            # print(outward)
            # type(outward)
            # print(outward.dc_number)
            print(outward_materials_r)
         
            for i in  outward_materials_r :
                print(i)
                print(i['product'])
                materials=outward_materials(outward_details=outward_details.objects.get(id=outward_r.id),tenant_id=i['tenant_id'],product =i['product'],qty=i['qty'],bal_qty=i['bal_qty'])
                materials.save()
                dispatch=Dispatch_materials.objects.filter(product_details=materials.product,dispatch_details=outward_r.dc_number).first()
                
                if dispatch :
                    print(materials.qty)
                    updated_qty=dispatch.bal_qty-float(materials.qty)
                    dispatch_details=Dispatch_materials.objects.filter(product_details=materials.product)
                    print(updated_qty)
                    dispatch_details.update(bal_qty=updated_qty)
            return Response('Success')
        else :
            print("serialization error")
               
            return Response('Error')
       
    
class Outwardmaterial_API(generics.GenericAPIView,APIView,mixins.ListModelMixin):
    serializer_class =outward_materials_serializers
    queryset= outward_materials.objects.all()
    
    def get(self,request):

        return self.list(request)