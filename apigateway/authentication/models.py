from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.fields.related import ForeignKey
from mptt.models import MPTTModel, TreeForeignKey
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
import smtplib
# Create your models here.


class AdminManager(models.Manager):
    def get_queryset(self, username):
        return super().get_queryset().filter(username=username, is_admin=True)


class EmployeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_employee=True)


class RolesManager(models.Manager):
    def get_queryset(self, username, roles):
        return super().get_queryset().filter(username=username, is_employee=True, roles=roles)


class Tenant_Company(models.Model):
    company_name = models.CharField(max_length=1024)
    address = models.TextField()
    phone_number = models.CharField(max_length=10)
    city = models.CharField(max_length=1024)
    state = models.CharField(max_length=1024)
    country = models.CharField(max_length=1024)
    joined_data = models.DateField(auto_now=True)
    domain = models.CharField(max_length=1024)

    def __str__(self):
        return (self.company_name)


class User(AbstractUser):

    tenant_company = models.ForeignKey(
        Tenant_Company, related_name='tenant_company', on_delete=models.CASCADE)

    is_admin = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=False)

    objects = UserManager()

    admin_objects = AdminManager()
    emp_objects = EmployeeManager()

    def __str__(self):
        return (self.username)


class emp_roles(models.Model):
    tenant_company = models.ForeignKey(
        Tenant_Company,on_delete=models.CASCADE)

    roles = models.CharField(max_length=1024)

    def __str__(self):
        return self.roles


class Employee(models.Model):
    tenant_company = models.ForeignKey(
        Tenant_Company,on_delete=models.CASCADE)

    employee = ForeignKey(User, on_delete=models.CASCADE)
    roles = models.ManyToManyField(emp_roles)
    objects = models.Manager()
    roles_manager = RolesManager()

    def __str__(self):
        return self.employee.username


class service(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    basic=models.BooleanField(default=False)
    inward=models.BooleanField(default=False)
    dispatch=models.BooleanField(default=False)
    production=models.BooleanField(default=False)
    billing=models.BooleanField(default=False)
    quality=models.BooleanField(default=False)

class menu_link_url(models.Model):
  link=models.CharField(max_length=1024)
  name=models.CharField(max_length=1024)
  service=models.CharField(max_length=1024)

  def __str__(self):
      return self.name
  

class menu_list(models.Model):
  user=models.ForeignKey(User, on_delete=models.CASCADE)
  name=models.CharField(max_length=1024)
  menu_link=models.ForeignKey(menu_link_url,related_name='menu_link',on_delete=models.CASCADE,default=1)
  parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)
  slug = models.SlugField(unique=True)

 

  class MPTTMeta:
    order_insertion_by = ['name']

  class Meta:
    unique_together = (('parent', 'slug',))
    verbose_name_plural = 'mainprocess'

  def get_slug_list(self):
    try:
      ancestors = self.get_ancestors(include_self=True)
    except:
      ancestors = []
    else:
      ancestors = [ i.slug for i in ancestors]
    slugs = []
    for i in range(len(ancestors)):
      slugs.append('/'.join(ancestors[:i+1]))
    return slugs

  def __str__(self):
    return self.name


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password:reset-password-request'), reset_password_token.key)
    content="You request is accepted succesfully"
    mail=smtplib.SMTP('smtp.gmail.com',587)
    mail.ehlo()
    mail.starttls()
    sender='kailasvs94@gmail.com'
    recipient=[reset_password_token.user.email]
    mail.login('kailasvs94@gmail.com','82@81@066@965')
    header='To:'+str(recipient)+'\n'+'From:'\
    +sender+'\n'+'Password Reset for {title}".format(title="Some website title")'
    content=header+content+email_plaintext_message
    mail.sendmail(sender,recipient,content)
    mail.close()
    # email_plaintext_message = "{}?token={}".format(reverse('password:reset-password-request'), reset_password_token.key)
    # mail=smtplib.SMTP('smtp.gmail.com',587)
    # mail.ehlo()
    # mail.starttls()
    # sender='kailasvs94@gmail.com'
    # mail.login('kailasvs94@gmail.com','82@81@066@965')
 
    # mail.sendmail(sender,"Password Reset for {title}".format(title="Some website title"), email_plaintext_message, [reset_password_token.user.email])
    #     # message:, content)
    # mail.close()
    # # send_mail(
    # #     # title:
    # #     "Password Reset for {title}".format(title="Some website title"),
    # #     # message:
    # #     email_plaintext_message,
    # #     # from:
    # #     "kailasvs94@gmail.com",
    # #     # to:
    # #     [reset_password_token.user.email]
    # # )