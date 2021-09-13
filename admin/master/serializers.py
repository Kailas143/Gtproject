from rest_framework import serializers

from .models import (Process, Processcost, Product, Productrequirements,
                     Productspec, Rawcomponent, company_details,
                     supliers_contact_details,Roles)


class RawcomponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rawcomponent
        fields = ('tenant_id','rname', 'code', 'grade', 'main_component', 'material','worker_name')

    def save(self):
        raw = Rawcomponent(
            tenant_id=self.validated_data.get('tenant_id'),
            worker_name=self.validated_data.get('worker_name'),
            rname=self.validated_data.get('rname'),
            code=self.validated_data.get('code'),
            grade=self.validated_data.get('grade'),
            main_component=self.validated_data.get('main_component'),
            material=self.validated_data.get('material')
        )
        raw.save()
        return raw


class RawcomponentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rawcomponent
        fields = ('rname', 'code', 'grade', 'main_component', 'material','worker_name')


class ProcesscostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processcost
        fields = '__all__'

    def save(self):
        processcost = Processcost(
            tenant_id=self.validated_data.get('tenant_id'),
            worker_name=self.validated_data.get('worker_name'),
            process_name=self.validated_data.get('process_name'),
            cycle_time=self.validated_data.get('cycle_time'),
            type_of_tools=self.validated_data.get('type_of_tools'),

        )
        processcost.save()
        return processcost


class ProcesscostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processcost
        fields = '__all__'


class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'

    def save(self):
        process = Process(
            tenant_id=self.validated_data.get('tenant_id'),
            worker_name=self.validated_data.get('worker_name'),
            process_name=self.validated_data.get('process_name'),
            test=self.validated_data.get('test'),
            cost=self.validated_data.get('cost'),

        )
        process.save()
        return process


class ProcessUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = '__all__'


class ProductspecSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productspec
        fields = '__all__'

    def save(self):
        spec = Productspec(
            worker_name=self.validated_data.get('worker_name'),
            spec=self.validated_data.get('spec'),
            value=self.validated_data.get('value'),
            unit=self.validated_data.get('unit'),

        )
        spec.save()
        return spec


class ProductspecUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productspec
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def save(self):
        prod = Product(
            tenant_id=self.validated_data.get('tenant_id'),
            worker_name=self.validated_data.get('worker_name'),
            pname=self.validated_data.get('pname'),
            billed_name=self.validated_data.get('billed_name'),
            cost=self.validated_data.get('cost'),
            IGST=self.validated_data.get('IGST'),
            SGST=self.validated_data.get('SGST'),
            CGST=self.validated_data.get('CGST'),
            code=self.validated_data.get('code'),
            job_name=self.validated_data.get('job_name'),
            main_component=self.validated_data.get('main_component'),
           
        )
        prod.save()
        return prod


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
class ProductrequSerializer(serializers.ModelSerializer):
     class Meta:
        model = Productrequirements
        fields = '__all__'

class ProductrequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productrequirements
        fields = ['product','raw_component','process','quantity']

    def save(self):
        prodreq = Productrequirements(
            product=self.validated_data.get('product'),
            tenant_id=self.validated_data.get('tenant_id'),
            worker_name=self.validated_data.get('worker_name'),
            raw_component=self.validated_data.get('raw_component'),
            process=self.validated_data.get('process'),
            quantity=self.validated_data.get('quantity'),

        )
        prodreq.save()
        return prodreq


class ProductUpdaterequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productrequirements
        fields = '__all__'


class Company_detailsSerializer(serializers.ModelSerializer):
    class Meta : 
        model = company_details
        fields = '__all__'
    
    def save(self):
        cd = company_details(
            tenant_id=self.validated_data.get('tenant_id'),
            worker_name=self.validated_data.get('worker_name'),
            company_name=self.validated_data.get('company_name'),
            address_line1=self.validated_data.get('address_line1'),
            address_line2=self.validated_data.get('address_line2'),
            address_line3=self.validated_data.get('address_line3'),
            office_email=self.validated_data.get('office_email'),
            office_pnone_no =self.validated_data.get('office_pnone_no '),
            gst_no=self.validated_data.get('gst_no'),
            acc_no=self.validated_data.get('acc_no'),
            ifsc_code=self.validated_data.get('ifsc_code'),
            bank_name=self.validated_data.get('bank_name'),
            branch_name=self.validated_data.get('quantity'),
            purchase_company=self.validated_data.get('purchase_company'),
            ratings=self.validated_data.get('ratings'),
            vendor_code=self.validated_data.get('vendor_code'),
            description=self.validated_data.get('description'),
                

        )
        cd.save()
        return cd
class Company_detailsUpdateSerializer(serializers.ModelSerializer):
    class Meta : 
        model = company_details
        fields = '__all__'

class Supliers_contactSerializer(serializers.ModelSerializer):
    class Meta :
        model = supliers_contact_details
        fields='__all__'
    
    def save(self):
        sup = supliers_contact_details(
            tenant_id=self.validated_data.get('tenant_id'),
            worker_name=self.validated_data.get('worker_name'),
            company_details=self.validated_data.get('company_details'),
            email=self.validated_data.get('email'),
            phone_no=self.validated_data.get('phone_no'),
            name=self.validated_data.get('name'),
            post =self.validated_data.get('post'),

        )
        sup.save()
        return sup
class  Supliers_contactUpdateSerializer(serializers.ModelSerializer):
    class Meta : 
        model = supliers_contact_details
        fields = '__all__'


class RolesSerializer(serializers.ModelSerializer) :
    class Meta :
        model = Roles
        fields='__all__'
       

# class UserSerializer(serializers.ModelSerializer) :
    
    
#     class Meta :
#         model = User
#         fields = ['username','email','password','roles']
        
    

