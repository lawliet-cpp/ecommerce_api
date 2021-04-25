from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

SIZES = (
    ("40 X 60","40 X 60"),
    ("100 X 200","100 X 200"),
    ("200 X 300","200 X 300")
)

class UserManager(BaseUserManager):

    def create_user(self,email=None,password=None,**extra_fields):
        if email ==None:
            return ValueError("You cannot create a user without the email")
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email=None,password=None,**extra_fields):
        user = self.model(email=email,**extra_fields)
        user.set_password(password)
        user.is_superuser =True
        user.is_staff = True
        user.save()
        return user



class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=155,unique=True)
    phone_number = models.PositiveIntegerField(unique=True,null=True)
    is_online = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    is_staff = models.BooleanField(default=False)
    username = None
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class CategoryManager(models.Manager):
    def get_products(self):
        products = Product.objects.filter(category=self.model)
        return products

class Category(models.Model):
    name = models.CharField(max_length=155,unique=True)
    objects = CategoryManager

class ProductManager(models.Manager):
    def isin_stock(self):
        if self.in_stock > 0:
            return True
        return False

class Product(models.Model):
    image = models.ImageField(upload_to="images",null=True)
    sizes = models.CharField(choices=SIZES,max_length=155,null=True)
    description = models.TextField(null=True)
    name = models.CharField(max_length=155)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True)
    price = models.PositiveIntegerField(null=True)
    in_stock = models.PositiveIntegerField(null=True)
    out_of_stock = models.BooleanField(default=False)
    objects = ProductManager


class OrderItem(models.Model):
    item = models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

class Order(models.Model):
    items = models.ManyToManyField(Product)
    country = models.CharField(max_length=155,null=True)
    adress = models.TextField(null=True)
    phone_number = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
    email = models.EmailField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)



@receiver(post_save,sender=User)
def token_signal(sender,instance,created,**kwargs):
    if created:
        Token.objects.create(user=instance)





