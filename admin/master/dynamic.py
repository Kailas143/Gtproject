from django.db import connection


def dynamic_link(api):
        # with connection['dynamic'].cursor() as cursor:
        #     cursor=cursor.execute("SELECT * FROM domain")
            
        #     print(cursor)

            
            domain_r="localhost"
            # print(domain_r)
            port="8000"
            scheme_url="http"
            # scheme_url = request.is_secure() and domain.url
            url = f"{scheme_url}://{domain_r}:{port}/{api}"
            print(url)

            return url