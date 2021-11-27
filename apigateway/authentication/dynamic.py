# import mysql.connector


# mydb=mysql.connector.connect(
#         host  = 'localhost',
#         user = 'root',
#         password ='password',
#         database ='dynamic_db', 
       
# )

# print(mydb,'---')

# mycursor=mydb.cursor()
# mycursor.execute("Select * from domain ")
# domain_details=mycursor.fetchall()

from django.db import connections

def dynamic_link(service,api):
    with connections['dynamic'].cursor() as mycursor:
        query="select * from domain WHERE services = '%s'" % service 
        mycursor.execute(query)
        domain_details=mycursor.fetchall()
        url = f"{domain_details[0][1]}://{domain_details[0][0]}:{domain_details[0][2]}/{api}/"
        print(url,'uu')
        return url
                
