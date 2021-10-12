import mysql.connector
from django.db.models import query

mydb=mysql.connector.connect(
        host  = 'localhost',
        user = 'root',
        password ='password',
        database ='dynamic_db', 
)
print(mydb)
mycursor=mydb.cursor()
mycursor.execute("Select * from domain ")
domain_details=mycursor.fetchall()
print(domain_details)
print(mycursor)


def dynamic_link(service,api):
    mycursor=mydb.cursor()
    query="select * from domain WHERE services = '%s'" % service 
    print(query)
  
    # val=services
    mycursor.execute(query)
    domain_details=mycursor.fetchall()
#     print(domain_details,'---------')
    
            # scheme_url = request.is_secure() and domain.url
    url = f"{domain_details[0][1]}://{domain_details[0][0]}:{domain_details[0][2]}/{api}/"
#     print(url,'----')

    return url
        
# with connection('dynamic').cursor() as cursor:
#         cursor=cursor.execute("SELECT * FROM domain")
            
#         print(cursor)